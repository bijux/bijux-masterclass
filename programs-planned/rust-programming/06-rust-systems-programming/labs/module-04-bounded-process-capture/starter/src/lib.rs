
#![forbid(unsafe_code)]

use std::ffi::OsString;

#[derive(Debug, Clone)]
pub struct CommandRequest {
    pub program: OsString,
    pub arguments: Vec<OsString>,
}

impl CommandRequest {
    pub fn new(program: impl Into<OsString>) -> Self {
        Self {
            program: program.into(),
            arguments: Vec::new(),
        }
    }

    pub fn argument(mut self, value: impl Into<OsString>) -> Self {
        self.arguments.push(value.into());
        self
    }
}

#[must_use]
pub fn display_for_humans(request: &CommandRequest) -> String {
    std::iter::once(&request.program)
        .chain(&request.arguments)
        .map(|value| format!("{value:?}"))
        .collect::<Vec<_>>()
        .join(" ")
}

#[cfg(test)]
mod tests {
    use super::{CommandRequest, display_for_humans};

    #[test]
    fn preserves_argument_boundaries() {
        let request = CommandRequest::new("tool").argument("a b");
        assert_eq!(request.arguments.len(), 1);
        assert!(display_for_humans(&request).contains("a b"));
    }
}
