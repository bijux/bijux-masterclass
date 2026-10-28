use crate::{broker::BrokerHandle, config::Config, domain::HealthState, error::ServiceError};
use bytes::Bytes;
use http_body_util::{BodyExt, Full};
use hyper::{
    body::Incoming,
    header::{CONNECTION, CONTENT_TYPE, HeaderValue},
    server::conn::http1,
    service::service_fn,
    Method, Request, Response, StatusCode,
};
use hyper_util::rt::TokioIo;
use std::{convert::Infallible, sync::Arc};
use tokio::{net::TcpListener, sync::Semaphore, task::JoinSet, time};
use tokio_util::sync::CancellationToken;

type ResponseBody = Full<Bytes>;

pub async fn serve_http(
    listener: TcpListener,
    broker: BrokerHandle,
    config: Config,
    shutdown: CancellationToken,
) -> Result<(), ServiceError> {
    let permits = Arc::new(Semaphore::new(config.max_http_connections));
    let mut connections = JoinSet::new();
    let mut fatal = None;

    loop {
        let permit = tokio::select! {
            () = shutdown.cancelled() => break,
            result = Arc::clone(&permits).acquire_owned() => match result {
                Ok(permit) => permit,
                Err(_) => break,
            }
        };
        let accepted = tokio::select! {
            () = shutdown.cancelled() => {
                drop(permit);
                break;
            }
            result = listener.accept() => result,
        };
        match accepted {
            Ok((stream, _peer)) => {
                let child_broker = broker.clone();
                let child_shutdown = shutdown.child_token();
                let _abort_handle = connections.spawn(async move {
                    let _permit = permit;
                    let io = TokioIo::new(stream);
                    let connection = http1::Builder::new().serve_connection(
                        io,
                        service_fn(move |request| route(request, child_broker.clone())),
                    );
                    tokio::pin!(connection);
                    tokio::select! {
                        result = &mut connection => result.map_err(ServiceError::from),
                        () = child_shutdown.cancelled() => {
                            connection.as_mut().graceful_shutdown();
                            connection.await.map_err(ServiceError::from)
                        }
                    }
                });
            }
            Err(error) => {
                drop(permit);
                fatal = Some(ServiceError::Io(error));
                break;
            }
        }
    }

    let drained = time::timeout(config.shutdown_grace, async {
        while connections.join_next().await.is_some() {}
    })
    .await;
    if drained.is_err() {
        connections.abort_all();
        while connections.join_next().await.is_some() {}
    }

    if let Some(error) = fatal {
        Err(error)
    } else {
        Ok(())
    }
}

pub async fn route(
    request: Request<Incoming>,
    broker: BrokerHandle,
) -> Result<Response<ResponseBody>, Infallible> {
    let (parts, body) = request.into_parts();
    let body_size = collect_body_size(body, 1024).await;
    let response = match body_size {
        Err(BodyPolicyError::TooLarge) => response(
            StatusCode::PAYLOAD_TOO_LARGE,
            "request body is not allowed\n".to_owned(),
            true,
        ),
        Err(BodyPolicyError::Transport) => response(
            StatusCode::BAD_REQUEST,
            "invalid request body\n".to_owned(),
            true,
        ),
        Ok(size) if size != 0 => response(
            StatusCode::BAD_REQUEST,
            "request body must be empty\n".to_owned(),
            false,
        ),
        Ok(_) => match (&parts.method, parts.uri.path()) {
            (&Method::GET, "/health") => {
                let snapshot = broker.snapshot();
                let status = if snapshot.health == HealthState::Ready {
                    StatusCode::OK
                } else {
                    StatusCode::SERVICE_UNAVAILABLE
                };
                response(status, format!("state={}\n", snapshot.health.as_str()), false)
            }
            (&Method::GET, "/stats") => {
                let snapshot = broker.snapshot();
                response(
                    StatusCode::OK,
                    format!(
                        "state={}\nactive_jobs={}\nqueued_jobs={}\nrecords={}\ncompleted_jobs={}\nfailed_jobs={}\n",
                        snapshot.health.as_str(),
                        snapshot.active_jobs,
                        snapshot.queued_jobs,
                        snapshot.records,
                        snapshot.completed_jobs,
                        snapshot.failed_jobs,
                    ),
                    false,
                )
            }
            (_, "/health" | "/stats") => response(
                StatusCode::METHOD_NOT_ALLOWED,
                "method not allowed\n".to_owned(),
                false,
            ),
            _ => response(StatusCode::NOT_FOUND, "not found\n".to_owned(), false),
        },
    };
    Ok(response)
}

#[derive(Debug)]
enum BodyPolicyError {
    TooLarge,
    Transport,
}

async fn collect_body_size(
    mut body: Incoming,
    maximum: usize,
) -> Result<usize, BodyPolicyError> {
    let mut total = 0_usize;
    while let Some(frame) = body.frame().await {
        let frame = frame.map_err(|_| BodyPolicyError::Transport)?;
        if let Ok(data) = frame.into_data() {
            total = total.checked_add(data.len()).ok_or(BodyPolicyError::TooLarge)?;
            if total > maximum {
                return Err(BodyPolicyError::TooLarge);
            }
        }
    }
    Ok(total)
}

fn response(status: StatusCode, body: String, close: bool) -> Response<ResponseBody> {
    let mut response = Response::new(Full::new(Bytes::from(body)));
    *response.status_mut() = status;
    let _previous = response.headers_mut().insert(
        CONTENT_TYPE,
        HeaderValue::from_static("text/plain; charset=utf-8"),
    );
    if close {
        let _previous = response
            .headers_mut()
            .insert(CONNECTION, HeaderValue::from_static("close"));
    }
    response
}
