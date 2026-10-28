use crate::parse::{BorrowedRecord, ParseError, parse_borrowed};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Request<'a> {
    Ingest(BorrowedRecord<'a>),
    Snapshot,
    Health,
    Quit,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ProtocolError {
    Empty,
    LineTooLong { actual: usize, maximum: usize },
    UnknownCommand,
    Record(ParseError),
}

impl fmt::Display for ProtocolError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Empty => formatter.write_str("empty command"),
            Self::LineTooLong { actual, maximum } => {
                write!(formatter, "command contains {actual} bytes; maximum is {maximum}")
            }
            Self::UnknownCommand => formatter.write_str("unsupported command"),
            Self::Record(error) => write!(formatter, "{error}"),
        }
    }
}

impl std::error::Error for ProtocolError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Record(error) => Some(error),
            _ => None,
        }
    }
}

pub fn parse_request(line: &str, max_line_bytes: usize) -> Result<Request<'_>, ProtocolError> {
    if line.is_empty() {
        return Err(ProtocolError::Empty);
    }
    if line.len() > max_line_bytes {
        return Err(ProtocolError::LineTooLong {
            actual: line.len(),
            maximum: max_line_bytes,
        });
    }
    if line == "SNAPSHOT" {
        return Ok(Request::Snapshot);
    }
    if line == "HEALTH" {
        return Ok(Request::Health);
    }
    if line == "QUIT" {
        return Ok(Request::Quit);
    }
    let Some(record_text) = line.strip_prefix("INGEST\t") else {
        return Err(ProtocolError::UnknownCommand);
    };
    let record = parse_borrowed(record_text, max_line_bytes).map_err(ProtocolError::Record)?;
    Ok(Request::Ingest(record))
}

pub fn public_error(error: &ProtocolError) -> (&'static str, &'static str) {
    match error {
        ProtocolError::Empty => ("EMPTY", "empty command"),
        ProtocolError::LineTooLong { .. } => {
            ("LINE_TOO_LONG", "line exceeds configured limit")
        }
        ProtocolError::UnknownCommand => ("UNKNOWN_COMMAND", "unsupported command"),
        ProtocolError::Record(_) => ("INVALID_RECORD", "invalid telemetry record"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_protocol_without_allocating_owned_identifiers() {
        let line = String::from("INGEST\tacme\trequests\t1\t2.5");
        let request = parse_request(&line, 128).expect("request");
        match request {
            Request::Ingest(record) => {
                assert_eq!(record.tenant, "acme");
                assert_eq!(record.metric, "requests");
            }
            _ => panic!("expected ingest"),
        }
    }

    #[test]
    fn public_error_does_not_echo_input() {
        let error = parse_request("SECRET-PAYLOAD", 128).expect_err("unknown");
        assert_eq!(
            public_error(&error),
            ("UNKNOWN_COMMAND", "unsupported command")
        );
    }

    #[test]
    fn direct_parser_enforces_the_complete_command_limit() {
        assert_eq!(
            parse_request("INGEST\ta\tb\t1\t2", 8),
            Err(ProtocolError::LineTooLong {
                actual: 14,
                maximum: 8,
            })
        );
    }
}
