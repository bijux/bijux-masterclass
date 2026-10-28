//! A deliberately small Hyper HTTP/1 operational surface.
//!
//! The HTTP layer does not own the application's business state. It reads a
//! snapshot from a watch channel and translates that state into bounded,
//! deterministic HTTP responses. Every accepted connection is tracked and
//! participates in service shutdown.

use std::{convert::Infallible, io, net::SocketAddr, sync::Arc, time::Duration};

use bytes::Bytes;
use http_body_util::{BodyExt, Full};
use hyper::{
    body::Incoming,
    header::{ALLOW, CONTENT_TYPE, HeaderValue},
    server::conn::http1,
    service::service_fn,
    Method, Request, Response, StatusCode,
};
use hyper_util::rt::TokioIo;
use tokio::{
    net::{TcpListener, TcpStream},
    sync::{Semaphore, watch},
    task::{JoinHandle, JoinSet},
    time,
};
use tokio_util::sync::CancellationToken;

pub type ResponseBody = Full<Bytes>;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Health {
    Starting,
    Ready,
    ShuttingDown,
    Failed,
}

impl Health {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Starting => "starting",
            Self::Ready => "ready",
            Self::ShuttingDown => "shutting-down",
            Self::Failed => "failed",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Snapshot {
    pub health: Health,
    pub active: usize,
    pub queued: usize,
}

#[derive(Debug, Clone, Copy)]
pub struct HttpLimits {
    pub max_connections: usize,
    pub max_body_bytes: usize,
    pub shutdown_grace: Duration,
}

impl HttpLimits {
    pub fn validate(self) -> io::Result<Self> {
        if !(1..=64).contains(&self.max_connections) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "max_connections must be in 1..=64",
            ));
        }
        if !(1..=4096).contains(&self.max_body_bytes) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "max_body_bytes must be in 1..=4096",
            ));
        }
        if self.shutdown_grace.is_zero() {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "shutdown_grace must be nonzero",
            ));
        }
        Ok(self)
    }
}

pub struct HttpService {
    address: SocketAddr,
    cancel: CancellationToken,
    task: JoinHandle<io::Result<()>>,
}

impl HttpService {
    pub async fn start(
        bind: SocketAddr,
        snapshots: watch::Receiver<Snapshot>,
        limits: HttpLimits,
    ) -> io::Result<Self> {
        let limits = limits.validate()?;
        let listener = TcpListener::bind(bind).await?;
        let address = listener.local_addr()?;
        let cancel = CancellationToken::new();
        let task = tokio::spawn(run_server(
            listener,
            snapshots,
            limits,
            cancel.child_token(),
        ));

        Ok(Self {
            address,
            cancel,
            task,
        })
    }

    pub fn local_addr(&self) -> SocketAddr {
        self.address
    }

    pub async fn shutdown(self) -> io::Result<()> {
        self.cancel.cancel();
        self.task.await.map_err(io::Error::other)?
    }
}

async fn run_server(
    listener: TcpListener,
    snapshots: watch::Receiver<Snapshot>,
    limits: HttpLimits,
    cancel: CancellationToken,
) -> io::Result<()> {
    let permits = Arc::new(Semaphore::new(limits.max_connections));
    let connection_cancel = CancellationToken::new();
    let mut connections = JoinSet::<io::Result<()>>::new();
    let mut first_error: Option<io::Error> = None;

    loop {
        tokio::select! {
            () = cancel.cancelled() => break,

            accepted = listener.accept() => {
                let (stream, _) = match accepted {
                    Ok(connection) => connection,
                    Err(error) => {
                        if first_error.is_none() {
                            first_error = Some(error);
                        }
                        break;
                    }
                };
                let Ok(permit) = Arc::clone(&permits).try_acquire_owned() else {
                    // Admission is intentionally fail-fast. Dropping the stream
                    // closes a connection that never committed to the service.
                    drop(stream);
                    continue;
                };

                let snapshot = snapshots.clone();
                let child_cancel = connection_cancel.child_token();
                let max_body_bytes = limits.max_body_bytes;
                let _abort_handle = connections.spawn(async move {
                    let _permit = permit;
                    serve_connection(stream, snapshot, max_body_bytes, child_cancel).await
                });
            }

            joined = connections.join_next(), if !connections.is_empty() => {
                if let Some(joined) = joined {
                    record_connection(joined, &mut first_error);
                }
            }
        }
    }

    connection_cancel.cancel();
    let deadline = time::Instant::now() + limits.shutdown_grace;

    while !connections.is_empty() {
        match time::timeout_at(deadline, connections.join_next()).await {
            Ok(Some(joined)) => record_connection(joined, &mut first_error),
            Ok(None) => break,
            Err(_) => break,
        }
    }

    if !connections.is_empty() {
        connections.abort_all();
        while let Some(joined) = connections.join_next().await {
            record_connection(joined, &mut first_error);
        }
    }

    match first_error {
        Some(error) => Err(error),
        None => Ok(()),
    }
}

async fn serve_connection(
    stream: TcpStream,
    snapshots: watch::Receiver<Snapshot>,
    max_body_bytes: usize,
    cancel: CancellationToken,
) -> io::Result<()> {
    let service = service_fn(move |request| {
        let snapshot = snapshots.borrow().clone();
        route(request, snapshot, max_body_bytes)
    });

    let io = TokioIo::new(stream);
    let mut connection = Box::pin(http1::Builder::new().serve_connection(io, service));

    tokio::select! {
        result = &mut connection => result.map_err(io::Error::other),
        () = cancel.cancelled() => {
            connection.as_mut().graceful_shutdown();
            connection.await.map_err(io::Error::other)
        }
    }
}

fn record_connection(
    joined: Result<io::Result<()>, tokio::task::JoinError>,
    first_error: &mut Option<io::Error>,
) {
    let error = match joined {
        Ok(Ok(())) => return,
        Ok(Err(error)) => error,
        Err(join_error) if join_error.is_cancelled() => return,
        Err(join_error) => io::Error::other(format!("connection task failed: {join_error}")),
    };

    if first_error.is_none() {
        *first_error = Some(error);
    }
}

pub async fn route(
    request: Request<Incoming>,
    snapshot: Snapshot,
    max_body_bytes: usize,
) -> Result<Response<ResponseBody>, Infallible> {
    let (parts, mut body) = request.into_parts();
    let mut body_bytes = 0usize;

    while let Some(frame) = body.frame().await {
        let frame = match frame {
            Ok(frame) => frame,
            Err(_) => return Ok(text_response(StatusCode::BAD_REQUEST, "invalid request body\n")),
        };

        if let Ok(data) = frame.into_data() {
            let Some(next) = body_bytes.checked_add(data.len()) else {
                return Ok(text_response(
                    StatusCode::PAYLOAD_TOO_LARGE,
                    "request body is too large\n",
                ));
            };
            body_bytes = next;
            if body_bytes > max_body_bytes {
                return Ok(text_response(
                    StatusCode::PAYLOAD_TOO_LARGE,
                    "request body is too large\n",
                ));
            }
        }
    }

    Ok(route_parts(
        &parts.method,
        parts.uri.path(),
        body_bytes,
        &snapshot,
    ))
}

pub fn route_parts(
    method: &Method,
    path: &str,
    body_bytes: usize,
    snapshot: &Snapshot,
) -> Response<ResponseBody> {
    if body_bytes != 0 {
        return text_response(StatusCode::BAD_REQUEST, "request body must be empty\n");
    }

    match (method, path) {
        (&Method::GET, "/health") => {
            let status = if snapshot.health == Health::Ready {
                StatusCode::OK
            } else {
                StatusCode::SERVICE_UNAVAILABLE
            };
            text_response(status, &format!("state={}\n", snapshot.health.as_str()))
        }
        (&Method::GET, "/stats") => text_response(
            StatusCode::OK,
            &format!(
                "state={}\nactive={}\nqueued={}\n",
                snapshot.health.as_str(),
                snapshot.active,
                snapshot.queued
            ),
        ),
        (_, "/health" | "/stats") => {
            let mut response = text_response(
                StatusCode::METHOD_NOT_ALLOWED,
                "method not allowed; use GET\n",
            );
            let _previous = response
                .headers_mut()
                .insert(ALLOW, HeaderValue::from_static("GET"));
            response
        }
        _ => text_response(StatusCode::NOT_FOUND, "not found\n"),
    }
}

fn text_response(status: StatusCode, text: &str) -> Response<ResponseBody> {
    let mut response = Response::new(Full::new(Bytes::copy_from_slice(text.as_bytes())));
    *response.status_mut() = status;
    let _previous = response.headers_mut().insert(
        CONTENT_TYPE,
        HeaderValue::from_static("text/plain; charset=utf-8"),
    );
    response
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::io::{AsyncReadExt, AsyncWriteExt};

    fn limits() -> HttpLimits {
        HttpLimits {
            max_connections: 4,
            max_body_bytes: 128,
            shutdown_grace: Duration::from_secs(1),
        }
    }

    #[test]
    fn pure_route_has_stable_method_and_health_policy() {
        let ready = Snapshot {
            health: Health::Ready,
            active: 2,
            queued: 3,
        };
        assert_eq!(
            route_parts(&Method::GET, "/health", 0, &ready).status(),
            StatusCode::OK
        );
        assert_eq!(
            route_parts(&Method::POST, "/health", 0, &ready).status(),
            StatusCode::METHOD_NOT_ALLOWED
        );
        assert_eq!(
            route_parts(&Method::GET, "/missing", 0, &ready).status(),
            StatusCode::NOT_FOUND
        );

        let starting = Snapshot {
            health: Health::Starting,
            active: 0,
            queued: 0,
        };
        assert_eq!(
            route_parts(&Method::GET, "/health", 0, &starting).status(),
            StatusCode::SERVICE_UNAVAILABLE
        );
    }

    #[tokio::test]
    async fn real_http_connection_reads_operational_snapshot() {
        let (_snapshot_tx, snapshot_rx) = watch::channel(Snapshot {
            health: Health::Ready,
            active: 7,
            queued: 2,
        });
        let service = HttpService::start(
            "127.0.0.1:0".parse().unwrap(),
            snapshot_rx,
            limits(),
        )
        .await
        .unwrap();

        let mut stream = TcpStream::connect(service.local_addr()).await.unwrap();
        stream
            .write_all(
                b"GET /stats HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n",
            )
            .await
            .unwrap();
        let mut response = Vec::new();
        stream.read_to_end(&mut response).await.unwrap();
        let response = String::from_utf8(response).unwrap();

        assert!(response.starts_with("HTTP/1.1 200 OK"));
        assert!(response.contains("state=ready\nactive=7\nqueued=2\n"));

        service.shutdown().await.unwrap();
    }

    #[tokio::test]
    async fn shutdown_joins_open_connections() {
        let (_snapshot_tx, snapshot_rx) = watch::channel(Snapshot {
            health: Health::ShuttingDown,
            active: 0,
            queued: 0,
        });
        let service = HttpService::start(
            "127.0.0.1:0".parse().unwrap(),
            snapshot_rx,
            limits(),
        )
        .await
        .unwrap();

        let _open_connection = TcpStream::connect(service.local_addr()).await.unwrap();
        service.shutdown().await.unwrap();
    }
}
