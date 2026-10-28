use crate::{
    broker::{BrokerHandle, SubmitReply, TerminalResult},
    codec::LengthCodec,
    config::Config,
    domain::JobRequest,
    error::ServiceError,
    protocol::{parse_client, render_server, ClientMessage, ServerMessage, VERSION},
};
use bytes::Bytes;
use futures_util::{SinkExt, StreamExt};
use std::{sync::Arc, time::Duration};
use tokio::{
    net::{TcpListener, TcpStream},
    sync::{OwnedSemaphorePermit, Semaphore},
    task::JoinSet,
    time,
};
use tokio_util::{codec::Framed, sync::CancellationToken};

pub async fn serve_tcp(
    listener: TcpListener,
    broker: BrokerHandle,
    config: Config,
    shutdown: CancellationToken,
) -> Result<(), ServiceError> {
    let permits = Arc::new(Semaphore::new(config.max_connections));
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
                let child = shutdown.child_token();
                let child_broker = broker.clone();
                let child_config = config.clone();
                let _abort_handle = connections.spawn(async move {
                    handle_connection(stream, permit, child_broker, child_config, child).await
                });
            }
            Err(error) => {
                drop(permit);
                fatal = Some(ServiceError::Io(error));
                break;
            }
        }
    }

    shutdown.cancel();
    drain_connections(&mut connections, config.shutdown_grace).await;
    if let Some(error) = fatal {
        Err(error)
    } else {
        Ok(())
    }
}

async fn drain_connections(
    connections: &mut JoinSet<Result<(), ServiceError>>,
    grace: Duration,
) {
    let drained = time::timeout(grace, async {
        while connections.join_next().await.is_some() {}
    })
    .await;
    if drained.is_err() {
        connections.abort_all();
        while connections.join_next().await.is_some() {}
    }
}

async fn handle_connection(
    stream: TcpStream,
    _permit: OwnedSemaphorePermit,
    broker: BrokerHandle,
    config: Config,
    shutdown: CancellationToken,
) -> Result<(), ServiceError> {
    let mut framed = Framed::new(stream, LengthCodec::new(config.max_frame_bytes));

    let first = match read_frame(&mut framed, config.handshake_timeout, "handshake").await {
        Ok(frame) => frame,
        Err(ServiceError::ConnectionClosed) => return Ok(()),
        Err(error) => return Err(error),
    };
    let first = parse_client(&first).map_err(|error| ServiceError::Protocol(error.to_string()))?;
    match first {
        ClientMessage::Hello { version: VERSION } => {
            send_message(
                &mut framed,
                ServerMessage::Welcome { version: VERSION },
                config.write_timeout,
            )
            .await?;
        }
        ClientMessage::Hello { .. } => {
            send_message(
                &mut framed,
                protocol_error(None, "UNSUPPORTED_VERSION", "server supports only version 1"),
                config.write_timeout,
            )
            .await?;
            return Ok(());
        }
        _ => {
            send_message(
                &mut framed,
                protocol_error(None, "HANDSHAKE_REQUIRED", "HELLO must be the first message"),
                config.write_timeout,
            )
            .await?;
            return Ok(());
        }
    }

    loop {
        let frame = tokio::select! {
            () = shutdown.cancelled() => return Ok(()),
            result = read_frame(&mut framed, config.request_timeout, "request") => match result {
                Ok(frame) => frame,
                Err(ServiceError::ConnectionClosed) => return Ok(()),
                Err(error) => return Err(error),
            }
        };

        let message = match parse_client(&frame) {
            Ok(message) => message,
            Err(error) => {
                send_message(
                    &mut framed,
                    protocol_error(None, error.code, &error.message),
                    config.write_timeout,
                )
                .await?;
                return Ok(());
            }
        };

        let response = match message {
            ClientMessage::Hello { .. } => {
                let response = protocol_error(None, "ALREADY_NEGOTIATED", "HELLO is legal only once");
                send_message(&mut framed, response, config.write_timeout).await?;
                return Ok(());
            }
            ClientMessage::Submit {
                request_id,
                idempotency_key,
                operation,
                payload,
            } => {
                let reply = time::timeout(
                    config.request_timeout,
                    broker.submit(JobRequest {
                        idempotency_key,
                        operation,
                        payload,
                    }),
                )
                .await
                .map_err(|_| ServiceError::Timeout("broker response"))?;
                map_submit_reply(request_id, reply)
            }
            ClientMessage::Stats { request_id } => ServerMessage::Stats {
                request_id,
                snapshot: broker.snapshot(),
            },
            ClientMessage::Ping { request_id } => ServerMessage::Pong { request_id },
            ClientMessage::Quit => {
                send_message(&mut framed, ServerMessage::Bye, config.write_timeout).await?;
                return Ok(());
            }
        };
        send_message(&mut framed, response, config.write_timeout).await?;
    }
}

async fn read_frame(
    framed: &mut Framed<TcpStream, LengthCodec>,
    timeout: Duration,
    stage: &'static str,
) -> Result<Bytes, ServiceError> {
    match time::timeout(timeout, framed.next()).await {
        Err(_) => Err(ServiceError::Timeout(stage)),
        Ok(None) => Err(ServiceError::ConnectionClosed),
        Ok(Some(Err(error))) => Err(ServiceError::Io(error)),
        Ok(Some(Ok(frame))) => Ok(frame),
    }
}

async fn send_message(
    framed: &mut Framed<TcpStream, LengthCodec>,
    message: ServerMessage,
    timeout: Duration,
) -> Result<(), ServiceError> {
    let bytes = Bytes::from(render_server(&message));
    time::timeout(timeout, framed.send(bytes))
        .await
        .map_err(|_| ServiceError::Timeout("response write"))??;
    Ok(())
}

fn map_submit_reply(request_id: String, reply: SubmitReply) -> ServerMessage {
    match reply {
        SubmitReply::Terminal(TerminalResult::Success(result)) => ServerMessage::Ok {
            request_id,
            value: result.value,
        },
        SubmitReply::Terminal(TerminalResult::DomainFailure(message)) => {
            protocol_error(Some(request_id), "JOB_FAILED", &message)
        }
        SubmitReply::Terminal(TerminalResult::Cancelled) => {
            protocol_error(Some(request_id), "JOB_CANCELLED", "job was cancelled")
        }
        SubmitReply::Busy { retry_after_ms } => ServerMessage::Busy {
            request_id,
            retry_after_ms,
        },
        SubmitReply::Conflict => protocol_error(
            Some(request_id),
            "IDEMPOTENCY_CONFLICT",
            "idempotency key was reused with different request content",
        ),
        SubmitReply::TooManyWaiters => protocol_error(
            Some(request_id),
            "TOO_MANY_WAITERS",
            "too many duplicate callers are waiting for this operation",
        ),
        SubmitReply::ShuttingDown => protocol_error(
            Some(request_id),
            "SHUTTING_DOWN",
            "service is not accepting new work",
        ),
    }
}

fn protocol_error(
    request_id: Option<String>,
    code: &str,
    message: &str,
) -> ServerMessage {
    ServerMessage::Error {
        request_id,
        code: code.to_owned(),
        message: message.replace('\t', " ").replace('\n', " "),
    }
}
