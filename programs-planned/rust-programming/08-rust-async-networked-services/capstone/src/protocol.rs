use crate::domain::{Operation, StatusSnapshot};
use std::{fmt, str::FromStr};

pub const VERSION: u16 = 1;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ClientMessage {
    Hello { version: u16 },
    Submit {
        request_id: String,
        idempotency_key: String,
        operation: Operation,
        payload: String,
    },
    Stats { request_id: String },
    Ping { request_id: String },
    Quit,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ServerMessage {
    Welcome { version: u16 },
    Ok { request_id: String, value: String },
    Busy { request_id: String, retry_after_ms: u64 },
    Error { request_id: Option<String>, code: String, message: String },
    Stats { request_id: String, snapshot: StatusSnapshot },
    Pong { request_id: String },
    Bye,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseError {
    pub code: &'static str,
    pub message: String,
}

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {}", self.code, self.message)
    }
}

impl std::error::Error for ParseError {}

fn validate_id(value: &str, field: &'static str) -> Result<String, ParseError> {
    if value.is_empty() || value.len() > 64 {
        return Err(ParseError {
            code: "INVALID_ARGUMENT",
            message: format!("{field} must contain 1..=64 bytes"),
        });
    }
    if !value.bytes().all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.')) {
        return Err(ParseError {
            code: "INVALID_ARGUMENT",
            message: format!("{field} contains unsupported characters"),
        });
    }
    Ok(value.to_owned())
}

pub fn parse_client(payload: &[u8]) -> Result<ClientMessage, ParseError> {
    let text = std::str::from_utf8(payload).map_err(|_| ParseError {
        code: "INVALID_UTF8",
        message: "frame payload must be UTF-8".to_owned(),
    })?;
    let fields: Vec<&str> = text.split('\t').collect();
    match fields.as_slice() {
        ["HELLO", version] => {
            let version = version.parse().map_err(|_| ParseError {
                code: "INVALID_ARGUMENT",
                message: "version must be an unsigned integer".to_owned(),
            })?;
            Ok(ClientMessage::Hello { version })
        }
        ["SUBMIT", request_id, key, operation, payload] => Ok(ClientMessage::Submit {
            request_id: validate_id(request_id, "request_id")?,
            idempotency_key: validate_id(key, "idempotency_key")?,
            operation: Operation::from_str(operation).map_err(|message| ParseError {
                code: "UNKNOWN_OPERATION",
                message: message.to_owned(),
            })?,
            payload: (*payload).to_owned(),
        }),
        ["STATS", request_id] => Ok(ClientMessage::Stats {
            request_id: validate_id(request_id, "request_id")?,
        }),
        ["PING", request_id] => Ok(ClientMessage::Ping {
            request_id: validate_id(request_id, "request_id")?,
        }),
        ["QUIT"] => Ok(ClientMessage::Quit),
        [] | [""] => Err(ParseError {
            code: "EMPTY_MESSAGE",
            message: "message is empty".to_owned(),
        }),
        _ => Err(ParseError {
            code: "INVALID_SYNTAX",
            message: "message does not match the JobWire V1 grammar".to_owned(),
        }),
    }
}

pub fn render_client(message: &ClientMessage) -> String {
    match message {
        ClientMessage::Hello { version } => format!("HELLO\t{version}"),
        ClientMessage::Submit { request_id, idempotency_key, operation, payload } => {
            format!("SUBMIT\t{request_id}\t{idempotency_key}\t{operation}\t{payload}")
        }
        ClientMessage::Stats { request_id } => format!("STATS\t{request_id}"),
        ClientMessage::Ping { request_id } => format!("PING\t{request_id}"),
        ClientMessage::Quit => "QUIT".to_owned(),
    }
}

pub fn parse_server(payload: &[u8]) -> Result<ServerMessage, ParseError> {
    let text = std::str::from_utf8(payload).map_err(|_| ParseError {
        code: "INVALID_UTF8",
        message: "response payload must be UTF-8".to_owned(),
    })?;
    let fields: Vec<&str> = text.split('\t').collect();
    match fields.as_slice() {
        ["WELCOME", version] => Ok(ServerMessage::Welcome {
            version: version.parse().map_err(|_| ParseError {
                code: "INVALID_RESPONSE",
                message: "WELCOME version is invalid".to_owned(),
            })?,
        }),
        ["OK", request_id, value] => Ok(ServerMessage::Ok {
            request_id: (*request_id).to_owned(),
            value: (*value).to_owned(),
        }),
        ["BUSY", request_id, retry] => Ok(ServerMessage::Busy {
            request_id: (*request_id).to_owned(),
            retry_after_ms: retry.parse().map_err(|_| ParseError {
                code: "INVALID_RESPONSE",
                message: "BUSY delay is invalid".to_owned(),
            })?,
        }),
        ["ERR", request_id, code, message] => Ok(ServerMessage::Error {
            request_id: (*request_id != "-").then(|| (*request_id).to_owned()),
            code: (*code).to_owned(),
            message: (*message).to_owned(),
        }),
        ["STATS-OK", request_id, health, active, queued, records, completed, failed] => {
            let parse_usize = |value: &str| value.parse::<usize>().map_err(|_| ParseError {
                code: "INVALID_RESPONSE",
                message: "STATS numeric field is invalid".to_owned(),
            });
            let parse_u64 = |value: &str| value.parse::<u64>().map_err(|_| ParseError {
                code: "INVALID_RESPONSE",
                message: "STATS numeric field is invalid".to_owned(),
            });
            Ok(ServerMessage::Stats {
                request_id: (*request_id).to_owned(),
                snapshot: StatusSnapshot {
                    health: crate::domain::HealthState::from_str(health).map_err(|_| ParseError {
                        code: "INVALID_RESPONSE",
                        message: "STATS health field is invalid".to_owned(),
                    })?,
                    active_jobs: parse_usize(active)?,
                    queued_jobs: parse_usize(queued)?,
                    records: parse_usize(records)?,
                    completed_jobs: parse_u64(completed)?,
                    failed_jobs: parse_u64(failed)?,
                },
            })
        }
        ["PONG", request_id] => Ok(ServerMessage::Pong {
            request_id: (*request_id).to_owned(),
        }),
        ["BYE"] => Ok(ServerMessage::Bye),
        _ => Err(ParseError {
            code: "INVALID_RESPONSE",
            message: "response does not match JobWire V1".to_owned(),
        }),
    }
}

pub fn render_server(message: &ServerMessage) -> String {
    match message {
        ServerMessage::Welcome { version } => format!("WELCOME\t{version}"),
        ServerMessage::Ok { request_id, value } => format!("OK\t{request_id}\t{value}"),
        ServerMessage::Busy { request_id, retry_after_ms } => {
            format!("BUSY\t{request_id}\t{retry_after_ms}")
        }
        ServerMessage::Error { request_id, code, message } => format!(
            "ERR\t{}\t{code}\t{message}",
            request_id.as_deref().unwrap_or("-")
        ),
        ServerMessage::Stats { request_id, snapshot } => format!(
            "STATS-OK\t{request_id}\t{}\t{}\t{}\t{}\t{}\t{}",
            snapshot.health.as_str(),
            snapshot.active_jobs,
            snapshot.queued_jobs,
            snapshot.records,
            snapshot.completed_jobs,
            snapshot.failed_jobs
        ),
        ServerMessage::Pong { request_id } => format!("PONG\t{request_id}"),
        ServerMessage::Bye => "BYE".to_owned(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn client_round_trip() {
        let message = ClientMessage::Submit {
            request_id: "r-1".to_owned(),
            idempotency_key: "k-1".to_owned(),
            operation: Operation::Uppercase,
            payload: "hello world".to_owned(),
        };
        assert_eq!(parse_client(render_client(&message).as_bytes()).unwrap(), message);
    }

    #[test]
    fn rejects_tabs_in_payload_by_arity() {
        let error = parse_client(b"SUBMIT\tr-1\tk-1\tuppercase\ta\tb").unwrap_err();
        assert_eq!(error.code, "INVALID_SYNTAX");
    }

    #[test]
    fn rejects_changed_identifier_alphabet() {
        let error = parse_client(b"PING\tbad id").unwrap_err();
        assert_eq!(error.code, "INVALID_ARGUMENT");
    }
}
