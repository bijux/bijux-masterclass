
//! Command-line application shell around the reusable systems library.

use crate::codec::Limits;
use crate::domain::{Archive, Entry, EntryKind, LogicalPath};
use crate::error::AppError;
use crate::path_policy::{sync_directory, write_new_file};
use crate::process_capture::{CapturePolicy, capture, encode_capture};
use crate::store::{load, save_atomic};
use std::ffi::{OsStr, OsString};
use std::fs;
use std::path::{Path, PathBuf};

pub const VERSION: &str = "0.1.0";

pub const HELP: &str = "FrameVault — versioned binary archives and shell-free command capture\n\
\n\
USAGE:\n\
    framevault create <archive.fv> <source>...\n\
    framevault create <archive.fv> --entry <logical-name> <source> [--entry ...]\n\
    framevault list <archive.fv>\n\
    framevault verify <archive.fv>\n\
    framevault extract <archive.fv> <directory>\n\
    framevault capture <archive.fv> -- <program> [argument...]\n\
    framevault help\n\
    framevault version\n\
\n\
NOTES:\n\
    Use `--entry <logical-name> <source>` for an explicit archive name.\n\
    Use `--source <source>` when a host path begins with `--`. Logical names\n\
    use `/`, are relative, and reject `.`, `..`, backslashes, drive markers,\n\
    empty components, NUL, and control characters.\n\
    Process execution does not use a shell. Captured output is accepted only\n\
    after the child exits; the storage limit is not a hard memory bound.\n\
    Extraction is per-file: earlier new files remain if a later entry fails.\n";

/// Successful command output and process exit status.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CommandResult {
    pub stdout: String,
    pub exit_code: i32,
}

fn os_to_path(value: &OsStr) -> PathBuf {
    PathBuf::from(value)
}

fn logical_for_source(argument: &OsStr) -> Result<(LogicalPath, PathBuf), AppError> {
    let source = PathBuf::from(argument);
    let file_name = source
        .file_name()
        .and_then(OsStr::to_str)
        .ok_or_else(|| AppError::NonUnicodeFileName(source.clone()))?;
    let logical = LogicalPath::parse(file_name).map_err(|source| AppError::InvalidLogicalPath {
        input: file_name.to_owned(),
        source,
    })?;
    Ok((logical, source))
}

fn explicit_logical_source(
    logical: &OsStr,
    source: &OsStr,
) -> Result<(LogicalPath, PathBuf), AppError> {
    let logical = logical
        .to_str()
        .ok_or_else(|| AppError::usage("logical names supplied after `--entry` must be Unicode"))?;
    let logical_path = LogicalPath::parse(logical).map_err(|source| {
        AppError::InvalidLogicalPath {
            input: logical.to_owned(),
            source,
        }
    })?;
    Ok((logical_path, PathBuf::from(source)))
}

fn read_source(path: &Path, limits: Limits) -> Result<Vec<u8>, AppError> {
    let metadata = fs::metadata(path).map_err(|source| AppError::io("inspect source", path, source))?;
    if !metadata.is_file() {
        return Err(AppError::usage(format!("source is not a regular file: {}", path.display())));
    }
    if metadata.len() > u64::try_from(limits.max_payload_bytes).unwrap_or(u64::MAX) {
        return Err(AppError::usage(format!(
            "source exceeds per-entry limit {}: {}",
            limits.max_payload_bytes,
            path.display()
        )));
    }
    fs::read(path).map_err(|source| AppError::io("read source", path, source))
}

fn create(arguments: &[OsString]) -> Result<CommandResult, AppError> {
    if arguments.len() < 2 {
        return Err(AppError::usage("create requires an archive path and at least one source"));
    }
    let destination = os_to_path(&arguments[0]);
    let limits = Limits::default();
    let mut archive = Archive::new();
    let mut index = 1;
    while index < arguments.len() {
        let (logical, source, consumed) = match arguments[index].to_str() {
            Some("--entry") => {
                let logical = arguments.get(index + 1).ok_or_else(|| {
                    AppError::usage("`--entry` requires a logical name and a source path")
                })?;
                let source = arguments.get(index + 2).ok_or_else(|| {
                    AppError::usage("`--entry` requires a logical name and a source path")
                })?;
                let (logical, source) = explicit_logical_source(logical, source)?;
                (logical, source, 3)
            }
            Some("--source") => {
                let source = arguments.get(index + 1).ok_or_else(|| {
                    AppError::usage("`--source` requires one host source path")
                })?;
                let (logical, source) = logical_for_source(source)?;
                (logical, source, 2)
            }
            _ => {
                let (logical, source) = logical_for_source(&arguments[index])?;
                (logical, source, 1)
            }
        };
        let payload = read_source(&source, limits)?;
        archive.push(Entry::new(EntryKind::File, logical, payload))?;
        index += consumed;
    }
    let outcome = save_atomic(&destination, &archive, limits)?;
    Ok(CommandResult {
        stdout: format!(
            "created\t{}\tentries={}\tfile_sync={}\tparent_sync={}\n",
            destination.display(),
            archive.entry_count(),
            outcome.file_synchronized,
            outcome.parent_directory_synchronized
        ),
        exit_code: 0,
    })
}

fn list(arguments: &[OsString]) -> Result<CommandResult, AppError> {
    if arguments.len() != 1 {
        return Err(AppError::usage("list requires exactly one archive path"));
    }
    let archive = load(&os_to_path(&arguments[0]), Limits::default())?;
    let mut output = String::from("index\tkind\tbytes\tname\n");
    for (index, entry) in archive.entries().iter().enumerate() {
        output.push_str(&format!(
            "{}\t{}\t{}\t{}\n",
            index + 1,
            entry.kind().label(),
            entry.payload_len(),
            entry.name()
        ));
    }
    Ok(CommandResult { stdout: output, exit_code: 0 })
}

fn verify(arguments: &[OsString]) -> Result<CommandResult, AppError> {
    if arguments.len() != 1 {
        return Err(AppError::usage("verify requires exactly one archive path"));
    }
    let archive_path = os_to_path(&arguments[0]);
    let archive = load(&archive_path, Limits::default())?;
    Ok(CommandResult {
        stdout: format!(
            "valid\t{}\tentries={}\tpayload_bytes={}\n",
            archive_path.display(),
            archive.entry_count(),
            archive.total_payload_bytes()
        ),
        exit_code: 0,
    })
}

fn extract(arguments: &[OsString]) -> Result<CommandResult, AppError> {
    if arguments.len() != 2 {
        return Err(AppError::usage("extract requires an archive path and destination directory"));
    }
    let archive = load(&os_to_path(&arguments[0]), Limits::default())?;
    let base = os_to_path(&arguments[1]);
    let mut output = String::new();
    for entry in archive.entries() {
        let destination = write_new_file(&base, entry.name(), entry.payload())?;
        if let Some(parent) = destination.parent() {
            sync_directory(parent)?;
        }
        output.push_str(&format!("extracted\t{}\n", destination.display()));
    }
    Ok(CommandResult { stdout: output, exit_code: 0 })
}

fn capture_command(arguments: &[OsString]) -> Result<CommandResult, AppError> {
    if arguments.len() < 3 || arguments[1].as_os_str() != OsStr::new("--") {
        return Err(AppError::usage(
            "capture requires `<archive.fv> -- <program> [argument...]`",
        ));
    }
    let destination = os_to_path(&arguments[0]);
    let program = &arguments[2];
    let child_arguments = &arguments[3..];
    let captured = capture(program, child_arguments, CapturePolicy::default())?;
    let payload = encode_capture(&captured)?;
    let name = LogicalPath::parse("captures/command.fvcmd").map_err(|source| {
        AppError::InvalidLogicalPath {
            input: "captures/command.fvcmd".to_owned(),
            source,
        }
    })?;
    let archive = Archive::from_entries(vec![Entry::new(
        EntryKind::CommandCapture,
        name,
        payload,
    )])?;
    save_atomic(&destination, &archive, Limits::default())?;
    Ok(CommandResult {
        stdout: format!(
            "captured\t{}\texit={}\tstdout={}\tstderr={}\n",
            captured.program,
            captured
                .exit_code
                .map_or_else(|| "signal-or-platform-status".to_owned(), |code| code.to_string()),
            captured.stdout.len(),
            captured.stderr.len()
        ),
        exit_code: 0,
    })
}

/// Parse and execute one command. Arguments do not include the executable name.
pub fn run(arguments: impl IntoIterator<Item = OsString>) -> Result<CommandResult, AppError> {
    let arguments: Vec<OsString> = arguments.into_iter().collect();
    let Some(command) = arguments.first().and_then(|value| value.to_str()) else {
        return Ok(CommandResult {
            stdout: HELP.to_owned(),
            exit_code: 0,
        });
    };
    let rest = &arguments[1..];
    match command {
        "create" => create(rest),
        "list" => list(rest),
        "verify" => verify(rest),
        "extract" => extract(rest),
        "capture" => capture_command(rest),
        "help" | "--help" | "-h" => Ok(CommandResult {
            stdout: HELP.to_owned(),
            exit_code: 0,
        }),
        "version" | "--version" | "-V" => Ok(CommandResult {
            stdout: format!("framevault {VERSION}\n"),
            exit_code: 0,
        }),
        other => Err(AppError::usage(format!("unknown command `{other}`\n\n{HELP}"))),
    }
}

#[cfg(test)]
mod tests {
    use super::{HELP, run};
    use std::ffi::OsString;

    #[test]
    fn no_arguments_returns_help() {
        let result = run(Vec::<OsString>::new()).expect("help succeeds");
        assert_eq!(result.exit_code, 0);
        assert_eq!(result.stdout, HELP);
    }

    #[test]
    fn unknown_command_is_usage_failure() {
        let error = run([OsString::from("mystery")]).expect_err("unknown command must fail");
        assert_eq!(error.exit_code(), 2);
    }
}
