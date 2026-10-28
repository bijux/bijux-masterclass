
#![forbid(unsafe_code)]

use std::ffi::OsString;
use std::fmt;
use std::path::PathBuf;
use std::process::Command;

#[derive(Debug, Clone)]
pub struct CommandRequest {
    pub program: OsString,
    pub arguments: Vec<OsString>,
    pub current_directory: Option<PathBuf>,
    pub clear_environment: bool,
    pub environment: Vec<(OsString, OsString)>,
}

impl CommandRequest {
    pub fn new(program: impl Into<OsString>) -> Self {
        Self {
            program: program.into(),
            arguments: Vec::new(),
            current_directory: None,
            clear_environment: false,
            environment: Vec::new(),
        }
    }

    pub fn argument(mut self, value: impl Into<OsString>) -> Self {
        self.arguments.push(value.into());
        self
    }

    pub fn current_directory(mut self, value: impl Into<PathBuf>) -> Self {
        self.current_directory = Some(value.into());
        self
    }

    pub fn clear_environment(mut self) -> Self {
        self.clear_environment = true;
        self
    }

    pub fn environment(mut self, key: impl Into<OsString>, value: impl Into<OsString>) -> Self {
        self.environment.push((key.into(), value.into()));
        self
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Status {
    Success,
    Exit(i32),
    Other,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Capture {
    pub status: Status,
    pub stdout: Vec<u8>,
    pub stderr: Vec<u8>,
}

#[derive(Debug)]
pub enum CaptureError {
    EmptyProgram,
    Spawn {
        program: OsString,
        source: std::io::Error,
    },
    SizeOverflow,
    OutputTooLarge {
        stdout: usize,
        stderr: usize,
        limit: usize,
    },
}

impl fmt::Display for CaptureError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for CaptureError {}

/// Capture a child process without a shell.
///
/// The size limit is checked after `Command::output` returns. It bounds accepted
/// stored output, not peak memory while a hostile child is running.
pub fn capture(request: &CommandRequest, limit: usize) -> Result<Capture, CaptureError> {
    if request.program.is_empty() {
        return Err(CaptureError::EmptyProgram);
    }

    let mut command = Command::new(&request.program);
    command.args(&request.arguments);
    if let Some(directory) = &request.current_directory {
        command.current_dir(directory);
    }
    if request.clear_environment {
        command.env_clear();
    }
    for (key, value) in &request.environment {
        command.env(key, value);
    }

    let output = command.output().map_err(|source| CaptureError::Spawn {
        program: request.program.clone(),
        source,
    })?;
    let total = output
        .stdout
        .len()
        .checked_add(output.stderr.len())
        .ok_or(CaptureError::SizeOverflow)?;
    if total > limit {
        return Err(CaptureError::OutputTooLarge {
            stdout: output.stdout.len(),
            stderr: output.stderr.len(),
            limit,
        });
    }

    let status = if output.status.success() {
        Status::Success
    } else if let Some(code) = output.status.code() {
        Status::Exit(code)
    } else {
        Status::Other
    };
    Ok(Capture {
        status,
        stdout: output.stdout,
        stderr: output.stderr,
    })
}

#[cfg(test)]
mod tests {
    use super::{CaptureError, CommandRequest, capture};

    #[test]
    fn captures_current_test_binary_help() {
        let executable = std::env::current_exe().expect("current executable");
        let result = capture(
            &CommandRequest::new(executable).argument("--help"),
            1024 * 1024,
        )
        .expect("capture succeeds");
        assert!(!result.stdout.is_empty() || !result.stderr.is_empty());
    }

    #[test]
    fn missing_program_is_structured() {
        let result = capture(&CommandRequest::new(""), 10);
        assert!(matches!(result, Err(CaptureError::EmptyProgram)));
    }
}
