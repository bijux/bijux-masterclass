//! A pure, version-negotiated command protocol.
//!
//! The implementation deliberately separates four responsibilities:
//!
//! 1. `parse` validates wire syntax and constructs a typed message.
//! 2. `render_message` and `render_reply` define canonical wire output.
//! 3. `transition` decides whether a typed message is legal in one state.
//! 4. `ProtocolError::close` records whether the current connection can
//!    continue after the error.

pub const SUPPORTED_VERSION: u16 = 1;
pub const MAX_REQUEST_ID_BYTES: usize = 32;
pub const MAX_TEXT_BYTES: usize = 256;
pub const MAX_UNKNOWN_FIELDS: usize = 8;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    Negotiating,
    Ready,
    Closing,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Message {
    Hello {
        version: u16,
    },
    Ping {
        request_id: String,
    },
    Echo {
        request_id: String,
        text: String,
    },
    Quit,
    Unknown {
        command: String,
        fields: Vec<String>,
    },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Reply {
    Welcome {
        version: u16,
    },
    Pong {
        request_id: String,
    },
    Echoed {
        request_id: String,
        text: String,
    },
    Bye,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProtocolError {
    pub code: &'static str,
    pub message: String,
    pub close: bool,
}

impl ProtocolError {
    fn new(code: &'static str, message: impl Into<String>, close: bool) -> Self {
        Self {
            code,
            message: message.into(),
            close,
        }
    }
}

pub fn parse(bytes: &[u8]) -> Result<Message, ProtocolError> {
    let text = std::str::from_utf8(bytes).map_err(|_| {
        ProtocolError::new("INVALID_UTF8", "payload is not valid UTF-8", true)
    })?;

    if text.is_empty() {
        return Err(ProtocolError::new(
            "EMPTY_MESSAGE",
            "a message must contain a command",
            true,
        ));
    }

    if text.bytes().any(|byte| matches!(byte, b'\r' | b'\n' | 0)) {
        return Err(ProtocolError::new(
            "INVALID_CONTROL",
            "framed messages cannot contain NUL, CR, or LF",
            true,
        ));
    }

    let fields: Vec<&str> = text.split('\t').collect();
    let command = fields[0];

    match (command, &fields[1..]) {
        ("HELLO", [version]) => {
            let version = version.parse::<u16>().map_err(|_| {
                ProtocolError::new(
                    "INVALID_VERSION",
                    "HELLO version must be an unsigned 16-bit integer",
                    true,
                )
            })?;
            Ok(Message::Hello { version })
        }
        ("PING", [request_id]) => {
            validate_request_id(request_id)?;
            Ok(Message::Ping {
                request_id: (*request_id).to_owned(),
            })
        }
        ("ECHO", [request_id, text]) => {
            validate_request_id(request_id)?;
            validate_text(text)?;
            Ok(Message::Echo {
                request_id: (*request_id).to_owned(),
                text: (*text).to_owned(),
            })
        }
        ("QUIT", []) => Ok(Message::Quit),
        ("HELLO" | "PING" | "ECHO" | "QUIT", _) => Err(ProtocolError::new(
            "INVALID_ARITY",
            format!("{command} received the wrong number of fields"),
            true,
        )),
        (unknown, rest) => {
            validate_command_name(unknown)?;
            if rest.len() > MAX_UNKNOWN_FIELDS {
                return Err(ProtocolError::new(
                    "TOO_MANY_FIELDS",
                    format!("unknown command {unknown} has too many fields"),
                    true,
                ));
            }

            let mut owned = Vec::with_capacity(rest.len());
            for field in rest {
                validate_opaque_field(field)?;
                owned.push((*field).to_owned());
            }

            Ok(Message::Unknown {
                command: unknown.to_owned(),
                fields: owned,
            })
        }
    }
}

pub fn render_message(message: &Message) -> String {
    match message {
        Message::Hello { version } => format!("HELLO\t{version}"),
        Message::Ping { request_id } => format!("PING\t{request_id}"),
        Message::Echo { request_id, text } => format!("ECHO\t{request_id}\t{text}"),
        Message::Quit => "QUIT".to_owned(),
        Message::Unknown { command, fields } => {
            let mut rendered = command.clone();
            for field in fields {
                rendered.push('\t');
                rendered.push_str(field);
            }
            rendered
        }
    }
}

pub fn render_reply(reply: &Reply) -> String {
    match reply {
        Reply::Welcome { version } => format!("WELCOME\t{version}"),
        Reply::Pong { request_id } => format!("PONG\t{request_id}"),
        Reply::Echoed { request_id, text } => format!("ECHOED\t{request_id}\t{text}"),
        Reply::Bye => "BYE".to_owned(),
    }
}

pub fn render_error(error: &ProtocolError) -> String {
    format!("ERROR\t{}\t{}", error.code, error.message)
}

pub fn transition(
    state: State,
    message: Message,
) -> Result<(State, Reply), ProtocolError> {
    match (state, message) {
        (State::Negotiating, Message::Hello { version: SUPPORTED_VERSION }) => Ok((
            State::Ready,
            Reply::Welcome {
                version: SUPPORTED_VERSION,
            },
        )),
        (State::Negotiating, Message::Hello { version }) => Err(ProtocolError::new(
            "UNSUPPORTED_VERSION",
            format!(
                "version {version} is unsupported; this server supports version {SUPPORTED_VERSION}"
            ),
            true,
        )),
        (State::Negotiating, _) => Err(ProtocolError::new(
            "HANDSHAKE_REQUIRED",
            "HELLO must be the first legal message",
            true,
        )),

        (State::Ready, Message::Hello { .. }) => Err(ProtocolError::new(
            "ALREADY_NEGOTIATED",
            "HELLO is legal exactly once",
            true,
        )),
        (State::Ready, Message::Ping { request_id }) => {
            Ok((State::Ready, Reply::Pong { request_id }))
        }
        (
            State::Ready,
            Message::Echo {
                request_id,
                text,
            },
        ) => Ok((State::Ready, Reply::Echoed { request_id, text })),
        (State::Ready, Message::Quit) => Ok((State::Closing, Reply::Bye)),
        (State::Ready, Message::Unknown { command, .. }) => Err(ProtocolError::new(
            "UNKNOWN_COMMAND",
            format!("command {command} is not defined by version {SUPPORTED_VERSION}"),
            false,
        )),

        (State::Closing, _) => Err(ProtocolError::new(
            "CLOSING",
            "no further messages are legal after QUIT",
            true,
        )),
    }
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
        Err(ProtocolError::new(
            "INVALID_ID",
            "request id must contain 1..=32 ASCII letters, digits, '-' or '_'",
            false,
        ))
    }
}

fn validate_text(value: &str) -> Result<(), ProtocolError> {
    if value.len() > MAX_TEXT_BYTES {
        return Err(ProtocolError::new(
            "TEXT_TOO_LARGE",
            format!("ECHO text exceeds {MAX_TEXT_BYTES} bytes"),
            false,
        ));
    }
    if value.bytes().any(|byte| matches!(byte, b'\t' | b'\r' | b'\n' | 0)) {
        return Err(ProtocolError::new(
            "INVALID_TEXT",
            "ECHO text cannot contain framing or field delimiters",
            false,
        ));
    }
    Ok(())
}

fn validate_command_name(value: &str) -> Result<(), ProtocolError> {
    let valid = !value.is_empty()
        && value.len() <= 24
        && value
            .bytes()
            .all(|byte| byte.is_ascii_uppercase() || byte == b'-');

    if valid {
        Ok(())
    } else {
        Err(ProtocolError::new(
            "INVALID_COMMAND",
            "command names must contain 1..=24 ASCII uppercase letters or '-'",
            true,
        ))
    }
}

fn validate_opaque_field(value: &str) -> Result<(), ProtocolError> {
    if value.len() > MAX_TEXT_BYTES {
        return Err(ProtocolError::new(
            "FIELD_TOO_LARGE",
            "unknown-command field exceeds the protocol bound",
            true,
        ));
    }
    if value.bytes().any(|byte| matches!(byte, b'\r' | b'\n' | 0)) {
        return Err(ProtocolError::new(
            "INVALID_FIELD",
            "unknown-command fields cannot contain NUL, CR, or LF",
            true,
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn message_round_trip_is_canonical() {
        let messages = [
            Message::Hello { version: 1 },
            Message::Ping {
                request_id: "r-17".to_owned(),
            },
            Message::Echo {
                request_id: "r_18".to_owned(),
                text: "hello, 世界".to_owned(),
            },
            Message::Quit,
            Message::Unknown {
                command: "FUTURE-COMMAND".to_owned(),
                fields: vec!["a".to_owned(), "b".to_owned()],
            },
        ];

        for message in messages {
            let wire = render_message(&message);
            assert_eq!(parse(wire.as_bytes()).unwrap(), message);
        }
    }

    #[test]
    fn invalid_utf8_and_wrong_arity_are_connection_fatal() {
        let utf8 = parse(&[0xff]).unwrap_err();
        assert_eq!(utf8.code, "INVALID_UTF8");
        assert!(utf8.close);

        let arity = parse(b"PING\tr1\textra").unwrap_err();
        assert_eq!(arity.code, "INVALID_ARITY");
        assert!(arity.close);
    }

    #[test]
    fn negotiation_is_required_and_happens_once() {
        let before = transition(
            State::Negotiating,
            Message::Ping {
                request_id: "r1".to_owned(),
            },
        )
        .unwrap_err();
        assert_eq!(before.code, "HANDSHAKE_REQUIRED");

        let (state, welcome) = transition(
            State::Negotiating,
            Message::Hello {
                version: SUPPORTED_VERSION,
            },
        )
        .unwrap();
        assert_eq!(state, State::Ready);
        assert_eq!(render_reply(&welcome), "WELCOME\t1");

        let repeated = transition(
            state,
            Message::Hello {
                version: SUPPORTED_VERSION,
            },
        )
        .unwrap_err();
        assert_eq!(repeated.code, "ALREADY_NEGOTIATED");
        assert!(repeated.close);
    }

    #[test]
    fn unknown_command_is_recoverable_only_after_negotiation() {
        let unknown = parse(b"FUTURE\tfield").unwrap();
        let error = transition(State::Ready, unknown).unwrap_err();
        assert_eq!(error.code, "UNKNOWN_COMMAND");
        assert!(!error.close);
    }

    #[test]
    fn quit_enters_terminal_protocol_state() {
        let (state, reply) = transition(State::Ready, Message::Quit).unwrap();
        assert_eq!(state, State::Closing);
        assert_eq!(reply, Reply::Bye);

        let error = transition(
            state,
            Message::Ping {
                request_id: "late".to_owned(),
            },
        )
        .unwrap_err();
        assert_eq!(error.code, "CLOSING");
    }
}
