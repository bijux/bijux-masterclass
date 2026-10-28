//! Starter surface for the negotiated command protocol laboratory.
//!
//! The starter defines the public vocabulary and the local validation rule.
//! You still need to design the wire grammar, parser, renderer, total state
//! transition, error taxonomy, close policy, and exhaustive tests.

pub const SUPPORTED_VERSION: u16 = 1;
pub const MAX_REQUEST_ID_BYTES: usize = 32;
pub const MAX_TEXT_BYTES: usize = 256;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    Negotiating,
    Ready,
    Closing,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Message {
    Hello { version: u16 },
    Ping { request_id: String },
    Echo { request_id: String, text: String },
    Quit,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProtocolError {
    pub code: &'static str,
    pub message: String,
    pub close: bool,
}

pub fn validate_request_id(value: &str) -> Result<(), ProtocolError> {
    let valid = !value.is_empty()
        && value.len() <= MAX_REQUEST_ID_BYTES
        && value
            .bytes()
            .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_'));

    if valid {
        Ok(())
    } else {
        Err(ProtocolError {
            code: "INVALID_ID",
            message: "request id must contain 1..=32 ASCII letters, digits, '-' or '_'"
                .to_owned(),
            close: false,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn request_id_policy_is_explicit() {
        assert!(validate_request_id("request-17_A").is_ok());
        assert!(validate_request_id("").is_err());
        assert!(validate_request_id("contains spaces").is_err());
        assert!(validate_request_id(&"x".repeat(33)).is_err());
    }
}
