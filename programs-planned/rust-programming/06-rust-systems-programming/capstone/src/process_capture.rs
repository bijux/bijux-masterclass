
//! Shell-free process execution and a portable capture payload.
//!
//! `Command::output` avoids shell parsing and drains both captured streams, but
//! it buffers output before this module can enforce its storage policy. The
//! configured limit is therefore a post-capture acceptance limit, not a hard
//! memory bound against a hostile child process.

use std::ffi::{OsStr, OsString};
use std::fmt;
use std::io;
use std::process::Command;

const MAGIC: &[u8; 8] = b"FVCMD01\0";

/// The stored outcome of one child process.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CommandCapture {
    pub program: String,
    pub arguments: Vec<String>,
    pub exit_code: Option<i32>,
    pub stdout: Vec<u8>,
    pub stderr: Vec<u8>,
}

/// Policy applied after the operating-system process API returns its output.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CapturePolicy {
    pub max_stored_output_bytes: usize,
}

impl Default for CapturePolicy {
    fn default() -> Self {
        Self {
            max_stored_output_bytes: 16 * 1024 * 1024,
        }
    }
}

/// A process-capture or capture-payload failure.
#[derive(Debug)]
pub enum CaptureError {
    EmptyProgram,
    NonUnicodeProgram,
    NonUnicodeArgument { index: usize },
    Spawn(io::Error),
    OutputTooLarge { observed: usize, limit: usize },
    TooManyArguments,
    TextTooLong,
    PayloadTooLong,
    InvalidPayload(&'static str),
    InvalidUtf8,
    NumericOverflow,
}

impl fmt::Display for CaptureError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyProgram => formatter.write_str("program name is empty"),
            Self::NonUnicodeProgram => formatter.write_str("program name is not Unicode and cannot enter the portable capture format"),
            Self::NonUnicodeArgument { index } => write!(formatter, "argument {index} is not Unicode and cannot enter the portable capture format"),
            Self::Spawn(error) => write!(formatter, "could not run child process: {error}"),
            Self::OutputTooLarge { observed, limit } => write!(formatter, "captured {observed} bytes, above storage limit {limit}"),
            Self::TooManyArguments => formatter.write_str("argument count does not fit the capture format"),
            Self::TextTooLong => formatter.write_str("program or argument text does not fit the capture format"),
            Self::PayloadTooLong => formatter.write_str("captured stream does not fit the capture format"),
            Self::InvalidPayload(message) => write!(formatter, "invalid process-capture payload: {message}"),
            Self::InvalidUtf8 => formatter.write_str("process-capture text is not UTF-8"),
            Self::NumericOverflow => formatter.write_str("process-capture number does not fit this host"),
        }
    }
}

impl std::error::Error for CaptureError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Spawn(error) => Some(error),
            _ => None,
        }
    }
}

/// Run one program directly, without a shell, and store its structured result.
pub fn capture(
    program: &OsStr,
    arguments: &[OsString],
    policy: CapturePolicy,
) -> Result<CommandCapture, CaptureError> {
    if program.is_empty() {
        return Err(CaptureError::EmptyProgram);
    }
    let portable_program = program
        .to_str()
        .ok_or(CaptureError::NonUnicodeProgram)?
        .to_owned();
    let portable_arguments = arguments
        .iter()
        .enumerate()
        .map(|(index, value)| {
            value
                .to_str()
                .map(str::to_owned)
                .ok_or(CaptureError::NonUnicodeArgument { index })
        })
        .collect::<Result<Vec<_>, _>>()?;

    let output = Command::new(program)
        .args(arguments)
        .output()
        .map_err(CaptureError::Spawn)?;
    let observed = output
        .stdout
        .len()
        .checked_add(output.stderr.len())
        .ok_or(CaptureError::NumericOverflow)?;
    if observed > policy.max_stored_output_bytes {
        return Err(CaptureError::OutputTooLarge {
            observed,
            limit: policy.max_stored_output_bytes,
        });
    }

    Ok(CommandCapture {
        program: portable_program,
        arguments: portable_arguments,
        exit_code: output.status.code(),
        stdout: output.stdout,
        stderr: output.stderr,
    })
}

fn push_text(output: &mut Vec<u8>, value: &str) -> Result<(), CaptureError> {
    let length = u32::try_from(value.len()).map_err(|_| CaptureError::TextTooLong)?;
    output.extend_from_slice(&length.to_le_bytes());
    output.extend_from_slice(value.as_bytes());
    Ok(())
}

/// Encode a command capture into a portable entry payload.
pub fn encode_capture(capture: &CommandCapture) -> Result<Vec<u8>, CaptureError> {
    let argument_count = u16::try_from(capture.arguments.len()).map_err(|_| CaptureError::TooManyArguments)?;
    let stdout_length = u64::try_from(capture.stdout.len()).map_err(|_| CaptureError::PayloadTooLong)?;
    let stderr_length = u64::try_from(capture.stderr.len()).map_err(|_| CaptureError::PayloadTooLong)?;

    let mut output = Vec::new();
    output.extend_from_slice(MAGIC);
    push_text(&mut output, &capture.program)?;
    output.extend_from_slice(&argument_count.to_le_bytes());
    for argument in &capture.arguments {
        push_text(&mut output, argument)?;
    }
    match capture.exit_code {
        Some(code) => {
            output.push(0);
            output.extend_from_slice(&code.to_le_bytes());
        }
        None => {
            output.push(1);
            output.extend_from_slice(&0_i32.to_le_bytes());
        }
    }
    output.extend_from_slice(&stdout_length.to_le_bytes());
    output.extend_from_slice(&stderr_length.to_le_bytes());
    output.extend_from_slice(&capture.stdout);
    output.extend_from_slice(&capture.stderr);
    Ok(output)
}

struct CaptureCursor<'a> {
    bytes: &'a [u8],
    position: usize,
}

impl<'a> CaptureCursor<'a> {
    const fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, position: 0 }
    }

    fn take(&mut self, length: usize) -> Result<&'a [u8], CaptureError> {
        let end = self.position.checked_add(length).ok_or(CaptureError::NumericOverflow)?;
        if end > self.bytes.len() {
            return Err(CaptureError::InvalidPayload("truncated field"));
        }
        let start = self.position;
        self.position = end;
        Ok(&self.bytes[start..end])
    }

    fn u8(&mut self) -> Result<u8, CaptureError> {
        Ok(self.take(1)?[0])
    }

    fn u16(&mut self) -> Result<u16, CaptureError> {
        let bytes = self.take(2)?;
        Ok(u16::from_le_bytes([bytes[0], bytes[1]]))
    }

    fn u32(&mut self) -> Result<u32, CaptureError> {
        let bytes = self.take(4)?;
        Ok(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }

    fn i32(&mut self) -> Result<i32, CaptureError> {
        let bytes = self.take(4)?;
        Ok(i32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }

    fn u64(&mut self) -> Result<u64, CaptureError> {
        let bytes = self.take(8)?;
        Ok(u64::from_le_bytes([
            bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7],
        ]))
    }

    fn text(&mut self) -> Result<String, CaptureError> {
        let length = usize::try_from(self.u32()?).map_err(|_| CaptureError::NumericOverflow)?;
        let bytes = self.take(length)?;
        std::str::from_utf8(bytes)
            .map(str::to_owned)
            .map_err(|_| CaptureError::InvalidUtf8)
    }
}

/// Decode a structured command-capture payload.
pub fn decode_capture(input: &[u8]) -> Result<CommandCapture, CaptureError> {
    let mut cursor = CaptureCursor::new(input);
    if cursor.take(MAGIC.len())? != MAGIC {
        return Err(CaptureError::InvalidPayload("invalid magic/version"));
    }
    let program = cursor.text()?;
    let argument_count = usize::from(cursor.u16()?);
    let mut arguments = Vec::new();
    arguments
        .try_reserve_exact(argument_count)
        .map_err(|_| CaptureError::PayloadTooLong)?;
    for _ in 0..argument_count {
        arguments.push(cursor.text()?);
    }
    let status_kind = cursor.u8()?;
    let status_value = cursor.i32()?;
    let exit_code = match status_kind {
        0 => Some(status_value),
        1 => None,
        _ => return Err(CaptureError::InvalidPayload("unknown status kind")),
    };
    let stdout_length = usize::try_from(cursor.u64()?).map_err(|_| CaptureError::NumericOverflow)?;
    let stderr_length = usize::try_from(cursor.u64()?).map_err(|_| CaptureError::NumericOverflow)?;
    let stdout = cursor.take(stdout_length)?.to_vec();
    let stderr = cursor.take(stderr_length)?.to_vec();
    if cursor.position != input.len() {
        return Err(CaptureError::InvalidPayload("trailing bytes"));
    }
    Ok(CommandCapture {
        program,
        arguments,
        exit_code,
        stdout,
        stderr,
    })
}

#[cfg(test)]
mod tests {
    use super::{CommandCapture, decode_capture, encode_capture};

    #[test]
    fn capture_payload_round_trips_without_textifying_streams() {
        let capture = CommandCapture {
            program: "tool".to_owned(),
            arguments: vec!["--raw".to_owned()],
            exit_code: Some(7),
            stdout: vec![0, 0xff, b'\n'],
            stderr: b"warning".to_vec(),
        };
        let bytes = encode_capture(&capture).expect("encodable capture");
        assert_eq!(decode_capture(&bytes), Ok(capture));
    }
}
