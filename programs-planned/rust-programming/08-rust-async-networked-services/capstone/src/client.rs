use crate::{
    codec::LengthCodec,
    domain::{JobResult, Operation, StatusSnapshot},
    error::ClientError,
    protocol::{parse_server, render_client, ClientMessage, ServerMessage, VERSION},
};
use bytes::Bytes;
use futures_util::{SinkExt, StreamExt};
use std::{net::SocketAddr, time::Duration};
use tokio::{net::TcpStream, time::{self, Instant}};
use tokio_util::codec::Framed;

pub struct JobWireClient {
    framed: Framed<TcpStream, LengthCodec>,
    timeout: Duration,
}

impl JobWireClient {
    pub async fn connect(
        address: SocketAddr,
        max_frame_bytes: usize,
        timeout: Duration,
    ) -> Result<Self, ClientError> {
        let stream = time::timeout(timeout, TcpStream::connect(address))
            .await
            .map_err(|_| ClientError::Timeout("connect"))??;
        let mut client = Self {
            framed: Framed::new(stream, LengthCodec::new(max_frame_bytes)),
            timeout,
        };
        let response = client.exchange(ClientMessage::Hello { version: VERSION }).await?;
        match response {
            ServerMessage::Welcome { version: VERSION } => Ok(client),
            other => Err(ClientError::Protocol(format!(
                "expected WELCOME 1, received {other:?}"
            ))),
        }
    }

    pub async fn submit(
        &mut self,
        request_id: String,
        idempotency_key: String,
        operation: Operation,
        payload: String,
    ) -> Result<JobResult, ClientError> {
        match self
            .exchange(ClientMessage::Submit {
                request_id: request_id.clone(),
                idempotency_key,
                operation,
                payload,
            })
            .await?
        {
            ServerMessage::Ok { request_id: actual, value } if actual == request_id => {
                Ok(JobResult { value })
            }
            ServerMessage::Busy { request_id: actual, retry_after_ms } if actual == request_id => {
                Err(ClientError::Busy { retry_after_ms })
            }
            ServerMessage::Error { request_id: actual, code, message }
                if actual.as_deref() == Some(request_id.as_str()) =>
            {
                Err(ClientError::Rejected { code, message })
            }
            other => Err(ClientError::Protocol(format!(
                "unexpected submit response: {other:?}"
            ))),
        }
    }

    pub async fn stats(&mut self, request_id: String) -> Result<StatusSnapshot, ClientError> {
        match self.exchange(ClientMessage::Stats { request_id: request_id.clone() }).await? {
            ServerMessage::Stats { request_id: actual, snapshot } if actual == request_id => {
                Ok(snapshot)
            }
            other => Err(ClientError::Protocol(format!(
                "unexpected stats response: {other:?}"
            ))),
        }
    }

    pub async fn ping(&mut self, request_id: String) -> Result<(), ClientError> {
        match self.exchange(ClientMessage::Ping { request_id: request_id.clone() }).await? {
            ServerMessage::Pong { request_id: actual } if actual == request_id => Ok(()),
            other => Err(ClientError::Protocol(format!(
                "unexpected ping response: {other:?}"
            ))),
        }
    }

    pub async fn quit(mut self) -> Result<(), ClientError> {
        match self.exchange(ClientMessage::Quit).await? {
            ServerMessage::Bye => Ok(()),
            other => Err(ClientError::Protocol(format!(
                "unexpected quit response: {other:?}"
            ))),
        }
    }

    async fn exchange(&mut self, message: ClientMessage) -> Result<ServerMessage, ClientError> {
        let encoded = Bytes::from(render_client(&message));
        time::timeout(self.timeout, self.framed.send(encoded))
            .await
            .map_err(|_| ClientError::Timeout("write"))??;
        let frame = time::timeout(self.timeout, self.framed.next())
            .await
            .map_err(|_| ClientError::Timeout("read"))?
            .ok_or_else(|| ClientError::Protocol("connection closed before response".to_owned()))??;
        parse_server(&frame).map_err(|error| ClientError::Protocol(error.to_string()))
    }
}

#[derive(Debug, Clone, Copy)]
pub struct RetryPolicy {
    pub max_attempts: u32,
    pub initial_delay: Duration,
    pub max_delay: Duration,
    pub overall_timeout: Duration,
}

impl Default for RetryPolicy {
    fn default() -> Self {
        Self {
            max_attempts: 4,
            initial_delay: Duration::from_millis(50),
            max_delay: Duration::from_millis(500),
            overall_timeout: Duration::from_secs(3),
        }
    }
}

impl RetryPolicy {
    fn validate(self) -> Result<Self, ClientError> {
        if self.max_attempts == 0 {
            return Err(ClientError::Protocol("retry policy requires at least one attempt".to_owned()));
        }
        if self.overall_timeout.is_zero() {
            return Err(ClientError::Protocol("retry policy requires a nonzero overall timeout".to_owned()));
        }
        if self.initial_delay > self.max_delay {
            return Err(ClientError::Protocol("initial retry delay exceeds maximum delay".to_owned()));
        }
        Ok(self)
    }
}

pub async fn submit_with_retry(
    address: SocketAddr,
    max_frame_bytes: usize,
    idempotency_key: String,
    operation: Operation,
    payload: String,
    policy: RetryPolicy,
) -> Result<JobResult, ClientError> {
    let policy = policy.validate()?;
    let deadline = Instant::now() + policy.overall_timeout;
    let mut delay = policy.initial_delay;
    let mut last_error = None;

    for attempt in 1..=policy.max_attempts {
        if Instant::now() >= deadline {
            break;
        }
        let attempt_deadline = std::cmp::min(
            deadline,
            Instant::now() + Duration::from_secs(1),
        );
        let stage_budget = attempt_deadline.saturating_duration_since(Instant::now());
        let result = match time::timeout_at(attempt_deadline, async {
            let mut client = JobWireClient::connect(address, max_frame_bytes, stage_budget).await?;
            client
                .submit(
                    format!("retry-{attempt}"),
                    idempotency_key.clone(),
                    operation,
                    payload.clone(),
                )
                .await
        })
        .await
        {
            Ok(result) => result,
            Err(_) => Err(ClientError::Timeout("retry attempt")),
        };

        match result {
            Ok(value) => return Ok(value),
            Err(error) if retryable(&error) && attempt < policy.max_attempts => {
                let scheduled_delay = match &error {
                    ClientError::Busy { retry_after_ms } => {
                        Duration::from_millis(*retry_after_ms).min(policy.max_delay)
                    }
                    _ => delay,
                };
                last_error = Some(error);
                let now = Instant::now();
                if now + scheduled_delay >= deadline {
                    break;
                }
                time::sleep(scheduled_delay).await;
                delay = delay.saturating_mul(2).min(policy.max_delay);
            }
            Err(error) => return Err(error),
        }
    }

    Err(last_error.unwrap_or(ClientError::Timeout("overall retry budget")))
}

fn retryable(error: &ClientError) -> bool {
    matches!(error, ClientError::Io(_) | ClientError::Timeout(_) | ClientError::Busy { .. })
}
