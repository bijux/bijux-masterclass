use crate::broker::{self, BrokerError, BrokerHandle};
use crate::config::Config;
use crate::metrics::Metrics;
use crate::parse::promote;
use crate::protocol::{Request, parse_request, public_error};
use crate::store::{Store, StoreError};
use bytes::BytesMut;
use std::fmt;
use std::io;
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::io::{AsyncBufRead, AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::{TcpListener, TcpStream};
use tokio::sync::{Semaphore, oneshot};
use tokio::task::{JoinHandle, JoinSet};
use tokio::time::{Duration, timeout};
use tracing::{Instrument, info, info_span, warn};

#[derive(Debug)]
pub enum ServerError {
    Io(io::Error),
    Task(String),
}

impl fmt::Display for ServerError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(formatter, "{error}"),
            Self::Task(message) => write!(formatter, "task failure: {message}"),
        }
    }
}

impl std::error::Error for ServerError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::Task(_) => None,
        }
    }
}

impl From<io::Error> for ServerError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

pub struct RunningServer {
    pub address: SocketAddr,
    shutdown: Option<oneshot::Sender<()>>,
    join: JoinHandle<Result<(), ServerError>>,
}

impl RunningServer {
    pub async fn shutdown(mut self) -> Result<(), ServerError> {
        if let Some(sender) = self.shutdown.take() {
            let _ = sender.send(());
        }
        self.join
            .await
            .map_err(|error| ServerError::Task(error.to_string()))?
    }
}

async fn read_bounded_line<R: AsyncBufRead + Unpin>(
    reader: &mut R,
    maximum: usize,
) -> io::Result<Option<BytesMut>> {
    let mut output = BytesMut::with_capacity(maximum.min(4096));
    loop {
        let (consumed, complete, too_long) = {
            let available = reader.fill_buf().await?;
            if available.is_empty() {
                return if output.is_empty() {
                    Ok(None)
                } else {
                    Ok(Some(output))
                };
            }

            let (data_length, consumed, complete) =
                if let Some(position) = available.iter().position(|&byte| byte == b'\n') {
                    (position, position + 1, true)
                } else {
                    (available.len(), available.len(), false)
                };
            let too_long = match output.len().checked_add(data_length) {
                Some(next_length) => next_length > maximum,
                None => true,
            };
            if !too_long {
                output.extend_from_slice(&available[..data_length]);
            }
            (consumed, complete, too_long)
        };

        reader.consume(consumed);
        if too_long {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "line exceeds configured limit",
            ));
        }
        if complete {
            if output.last() == Some(&b'\r') {
                output.truncate(output.len() - 1);
            }
            return Ok(Some(output));
        }
    }
}

async fn write_bytes(
    stream: &mut tokio::net::tcp::OwnedWriteHalf,
    bytes: &[u8],
    write_timeout: Duration,
) -> io::Result<()> {
    timeout(write_timeout, async {
        stream.write_all(bytes).await?;
        stream.flush().await
    })
    .await
    .map_err(|_| io::Error::new(io::ErrorKind::TimedOut, "response write deadline exceeded"))?
}

async fn write_line(
    stream: &mut tokio::net::tcp::OwnedWriteHalf,
    line: &str,
    write_timeout: Duration,
) -> io::Result<()> {
    timeout(write_timeout, async {
        stream.write_all(line.as_bytes()).await?;
        stream.write_all(b"\n").await?;
        stream.flush().await
    })
    .await
    .map_err(|_| io::Error::new(io::ErrorKind::TimedOut, "response write deadline exceeded"))?
}

async fn handle_connection(
    stream: TcpStream,
    connection_id: u64,
    config: Config,
    broker: BrokerHandle,
    metrics: Arc<Metrics>,
) -> Result<(), ServerError> {
    metrics.connection_opened();
    let _guard = ConnectionGuard(Arc::clone(&metrics));
    let (read, mut write) = stream.into_split();
    let mut reader = BufReader::new(read);
    let span = info_span!("connection", connection_id);
    let idle_timeout = Duration::from_millis(config.connection_idle_timeout_ms);
    let write_timeout = Duration::from_millis(config.write_timeout_ms);

    async move {
        loop {
            let line = match timeout(
                idle_timeout,
                read_bounded_line(&mut reader, config.max_line_bytes),
            )
            .await
            {
                Err(_) => {
                    write_line(
                        &mut write,
                        "ERR\tIDLE_TIMEOUT\tconnection idle deadline exceeded",
                        write_timeout,
                    )
                    .await?;
                    return Ok(());
                }
                Ok(Ok(Some(line))) => line,
                Ok(Ok(None)) => return Ok(()),
                Ok(Err(error)) if error.kind() == io::ErrorKind::InvalidData => {
                    metrics.invalid();
                    write_line(
                        &mut write,
                        "ERR\tLINE_TOO_LONG\tline exceeds configured limit",
                        write_timeout,
                    )
                    .await?;
                    return Ok(());
                }
                Ok(Err(error)) => return Err(ServerError::Io(error)),
            };

            let line = match std::str::from_utf8(&line) {
                Ok(line) => line,
                Err(_) => {
                    metrics.invalid();
                    write_line(
                        &mut write,
                        "ERR\tINVALID_UTF8\tcommand must be UTF-8",
                        write_timeout,
                    )
                    .await?;
                    continue;
                }
            };
            let request = match parse_request(line, config.max_line_bytes) {
                Ok(request) => request,
                Err(error) => {
                    metrics.invalid();
                    let (code, message) = public_error(&error);
                    write_line(
                        &mut write,
                        &format!("ERR\t{code}\t{message}"),
                        write_timeout,
                    )
                    .await?;
                    continue;
                }
            };

            match request {
                Request::Ingest(borrowed) => {
                    let record = match promote(borrowed, config.max_identifier_bytes) {
                        Ok(record) => record,
                        Err(_) => {
                            metrics.invalid();
                            write_line(
                                &mut write,
                                "ERR\tINVALID_RECORD\tinvalid telemetry record",
                                write_timeout,
                            )
                            .await?;
                            continue;
                        }
                    };
                    match broker.ingest(record).await {
                        Ok(()) => write_line(&mut write, "OK", write_timeout).await?,
                        Err(BrokerError::Overloaded) => {
                            write_line(
                                &mut write,
                                "ERR\tOVERLOADED\tservice is at capacity",
                                write_timeout,
                            )
                            .await?;
                        }
                        Err(BrokerError::Store(StoreError::Domain(_))) => {
                            metrics.invalid();
                            write_line(
                                &mut write,
                                "ERR\tINVALID_RECORD\trecord rejected",
                                write_timeout,
                            )
                            .await?;
                        }
                        Err(BrokerError::Store(
                            StoreError::SeriesLimit | StoreError::IdentifierStorageLimit,
                        )) => {
                            metrics.overloaded();
                            write_line(
                                &mut write,
                                "ERR\tCAPACITY\tstore capacity reached",
                                write_timeout,
                            )
                            .await?;
                        }
                        Err(BrokerError::Store(StoreError::SnapshotTooLarge)) => {
                            write_line(
                                &mut write,
                                "ERR\tINTERNAL\tunexpected store failure",
                                write_timeout,
                            )
                            .await?;
                        }
                        Err(BrokerError::Closed) => {
                            write_line(
                                &mut write,
                                "ERR\tUNAVAILABLE\tservice is shutting down",
                                write_timeout,
                            )
                            .await?;
                            return Ok(());
                        }
                    }
                }
                Request::Snapshot => {
                    let snapshot = match broker.snapshot().await {
                        Ok(snapshot) => snapshot,
                        Err(BrokerError::Overloaded) => {
                            write_line(
                                &mut write,
                                "ERR\tOVERLOADED\tservice is at capacity",
                                write_timeout,
                            )
                            .await?;
                            continue;
                        }
                        Err(_) => {
                            write_line(
                                &mut write,
                                "ERR\tUNAVAILABLE\tservice is shutting down",
                                write_timeout,
                            )
                            .await?;
                            return Ok(());
                        }
                    };
                    let rendered = match snapshot.render(config.max_snapshot_bytes) {
                        Ok(rendered) => rendered,
                        Err(_) => {
                            write_line(
                                &mut write,
                                "ERR\tSNAPSHOT_TOO_LARGE\tsnapshot exceeds limit",
                                write_timeout,
                            )
                            .await?;
                            continue;
                        }
                    };
                    write_line(
                        &mut write,
                        &format!("SNAPSHOT-BEGIN\t{}", snapshot.rows.len()),
                        write_timeout,
                    )
                    .await?;
                    write_bytes(&mut write, rendered.as_bytes(), write_timeout).await?;
                    write_line(&mut write, "SNAPSHOT-END", write_timeout).await?;
                    metrics.snapshot_completed();
                }
                Request::Health => {
                    let series = match broker.series_count().await {
                        Ok(series) => series,
                        Err(BrokerError::Overloaded) => {
                            write_line(
                                &mut write,
                                "DEGRADED\tbroker-overloaded",
                                write_timeout,
                            )
                            .await?;
                            continue;
                        }
                        Err(_) => {
                            write_line(
                                &mut write,
                                "UNHEALTHY\tbroker-unavailable",
                                write_timeout,
                            )
                            .await?;
                            return Ok(());
                        }
                    };
                    let current = metrics.snapshot();
                    write_line(
                        &mut write,
                        &format!(
                            "HEALTHY\t{}\t{}\t{}",
                            current.active_connections_observed,
                            current.queue_depth_observed,
                            series
                        ),
                        write_timeout,
                    )
                    .await?;
                }
                Request::Quit => {
                    write_line(&mut write, "BYE", write_timeout).await?;
                    return Ok(());
                }
            }
        }
    }
    .instrument(span)
    .await
}

struct ConnectionGuard(Arc<Metrics>);

impl Drop for ConnectionGuard {
    fn drop(&mut self) {
        self.0.connection_closed();
    }
}

pub async fn spawn(address: &str, config: Config) -> Result<RunningServer, ServerError> {
    config.validate().map_err(|error| {
        ServerError::Io(io::Error::new(
            io::ErrorKind::InvalidInput,
            error.to_string(),
        ))
    })?;
    let listener = TcpListener::bind(address).await?;
    let address = listener.local_addr()?;
    let metrics = Arc::new(Metrics::default());
    let store = Store::new(config.max_series, config.max_identifier_storage_bytes);
    let (broker, task) = broker::channel(
        config.mailbox_capacity,
        config.max_active_ingest,
        store,
        Arc::clone(&metrics),
    );
    let broker_join = tokio::spawn(task.run());
    let permits = Arc::new(Semaphore::new(config.max_connections));
    let (shutdown, mut shutdown_rx) = oneshot::channel::<()>();
    let grace = Duration::from_millis(config.shutdown_grace_ms);

    let join = tokio::spawn(async move {
        let mut connections = JoinSet::new();
        let mut next_id = 1_u64;
        loop {
            tokio::select! {
                _ = &mut shutdown_rx => break,
                accepted = listener.accept() => {
                    let (stream, peer) = accepted?;
                    let permit = match Arc::clone(&permits).try_acquire_owned() {
                        Ok(permit) => permit,
                        Err(_) => {
                            metrics.overloaded();
                            warn!(%peer, "connection rejected at admission");
                            let _ = stream.try_write(
                                b"ERR\tOVERLOADED\tconnection capacity reached\n",
                            );
                            continue;
                        }
                    };
                    let local_config = config.clone();
                    let local_broker = broker.clone();
                    let local_metrics = Arc::clone(&metrics);
                    let connection_id = next_id;
                    next_id = next_id
                        .checked_add(1)
                        .ok_or_else(|| ServerError::Task("connection identifier exhausted".into()))?;
                    connections.spawn(async move {
                        let _permit = permit;
                        handle_connection(
                            stream,
                            connection_id,
                            local_config,
                            local_broker,
                            local_metrics,
                        )
                        .await
                    });
                }
            }
        }

        info!("listener quiesced");
        let deadline = tokio::time::Instant::now() + grace;
        while !connections.is_empty() {
            tokio::select! {
                result = connections.join_next() => {
                    match result {
                        Some(Ok(Ok(()))) => {}
                        Some(Ok(Err(error))) => warn!(?error, "connection failed"),
                        Some(Err(error)) => warn!(?error, "connection task panicked"),
                        None => break,
                    }
                }
                _ = tokio::time::sleep_until(deadline) => {
                    connections.abort_all();
                    while connections.join_next().await.is_some() {}
                    break;
                }
            }
        }
        let _ = broker.shutdown().await;
        broker_join
            .await
            .map_err(|error| ServerError::Task(error.to_string()))?;
        Ok(())
    });

    Ok(RunningServer {
        address,
        shutdown: Some(shutdown),
        join,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn server_starts_on_ephemeral_port_and_shuts_down() {
        let server = spawn("127.0.0.1:0", Config::default())
            .await
            .expect("server");
        assert_ne!(server.address.port(), 0);
        server.shutdown().await.expect("shutdown");
    }
}
