
//! Extraction-path policy and the limits of pathname-based containment.
//!
//! FrameVault rejects dangerous lexical syntax and refuses existing symlink
//! ancestors. Those checks reduce accidental escape and common archive attacks,
//! but pathname preflight cannot prove containment against an adversary that
//! races the filesystem between inspection and creation. Descriptor-relative
//! operating-system APIs are required for that stronger threat model.

use crate::domain::LogicalPath;
use std::fmt;
use std::fs::{self, OpenOptions};
#[cfg(unix)]
use std::fs::File;
use std::io::{self, Write};
use std::path::{Path, PathBuf};

/// A failure while preparing or writing an extraction destination.
#[derive(Debug)]
pub enum PathPolicyError {
    BaseIsSymlink(PathBuf),
    AncestorIsSymlink(PathBuf),
    AncestorIsNotDirectory(PathBuf),
    DestinationExists(PathBuf),
    Io {
        operation: &'static str,
        path: PathBuf,
        source: io::Error,
    },
}

impl PathPolicyError {
    fn io(operation: &'static str, path: impl Into<PathBuf>, source: io::Error) -> Self {
        Self::Io {
            operation,
            path: path.into(),
            source,
        }
    }
}

impl fmt::Display for PathPolicyError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::BaseIsSymlink(path) => write!(formatter, "extraction base is a symlink: {}", path.display()),
            Self::AncestorIsSymlink(path) => write!(formatter, "extraction ancestor is a symlink: {}", path.display()),
            Self::AncestorIsNotDirectory(path) => write!(formatter, "extraction ancestor is not a directory: {}", path.display()),
            Self::DestinationExists(path) => write!(formatter, "extraction destination already exists: {}", path.display()),
            Self::Io { operation, path, source } => {
                write!(formatter, "could not {operation} `{}`: {source}", path.display())
            }
        }
    }
}

impl std::error::Error for PathPolicyError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Io { source, .. } => Some(source),
            _ => None,
        }
    }
}

fn inspect_existing_directory(path: &Path, base: bool) -> Result<(), PathPolicyError> {
    match fs::symlink_metadata(path) {
        Ok(metadata) => {
            if metadata.file_type().is_symlink() {
                return if base {
                    Err(PathPolicyError::BaseIsSymlink(path.to_path_buf()))
                } else {
                    Err(PathPolicyError::AncestorIsSymlink(path.to_path_buf()))
                };
            }
            if !metadata.is_dir() {
                return Err(PathPolicyError::AncestorIsNotDirectory(path.to_path_buf()));
            }
            Ok(())
        }
        Err(error) if error.kind() == io::ErrorKind::NotFound => {
            fs::create_dir(path).map_err(|source| PathPolicyError::io("create directory", path, source))?;
            let metadata = fs::symlink_metadata(path)
                .map_err(|source| PathPolicyError::io("inspect created directory", path, source))?;
            if metadata.file_type().is_symlink() {
                return if base {
                    Err(PathPolicyError::BaseIsSymlink(path.to_path_buf()))
                } else {
                    Err(PathPolicyError::AncestorIsSymlink(path.to_path_buf()))
                };
            }
            if !metadata.is_dir() {
                return Err(PathPolicyError::AncestorIsNotDirectory(path.to_path_buf()));
            }
            Ok(())
        }
        Err(source) => Err(PathPolicyError::io("inspect directory", path, source)),
    }
}

/// Prepare the parent directories and return the final host path.
///
/// This function performs lexical validation through `LogicalPath`, rejects
/// existing symlink ancestors, and creates missing directories one component at
/// a time. It is not an adversarial race-proof sandbox.
pub fn prepare_destination(base: &Path, logical: &LogicalPath) -> Result<PathBuf, PathPolicyError> {
    if base.exists() {
        inspect_existing_directory(base, true)?;
    } else {
        fs::create_dir_all(base)
            .map_err(|source| PathPolicyError::io("create extraction base", base, source))?;
        inspect_existing_directory(base, true)?;
    }

    let components: Vec<&str> = logical.components().collect();
    let mut current = base.to_path_buf();
    for component in &components[..components.len() - 1] {
        current.push(component);
        inspect_existing_directory(&current, false)?;
    }

    let destination = current.join(components[components.len() - 1]);
    match fs::symlink_metadata(&destination) {
        Ok(_) => Err(PathPolicyError::DestinationExists(destination)),
        Err(error) if error.kind() == io::ErrorKind::NotFound => Ok(destination),
        Err(source) => Err(PathPolicyError::io("inspect destination", destination, source)),
    }
}


fn persist_new_file(file: &mut std::fs::File, payload: &[u8]) -> io::Result<()> {
    file.write_all(payload)?;
    file.flush()?;
    file.sync_all()
}

/// Write one new extracted file without overwriting an existing object.
pub fn write_new_file(
    base: &Path,
    logical: &LogicalPath,
    payload: &[u8],
) -> Result<PathBuf, PathPolicyError> {
    let destination = prepare_destination(base, logical)?;
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&destination)
        .map_err(|source| {
            if source.kind() == io::ErrorKind::AlreadyExists {
                PathPolicyError::DestinationExists(destination.clone())
            } else {
                PathPolicyError::io("create destination", &destination, source)
            }
        })?;

    let result = persist_new_file(&mut file, payload);

    if let Err(source) = result {
        drop(file);
        let _ = fs::remove_file(&destination);
        return Err(PathPolicyError::io("write destination", destination, source));
    }

    Ok(destination)
}

/// Best-effort directory synchronization used after creating extraction files.
///
/// Directory synchronization is attempted only on Unix, where opening a
/// directory as a `File` is commonly supported. Failure is reported rather than
/// silently converted into a durability claim.
#[cfg(unix)]
pub fn sync_directory(path: &Path) -> Result<(), PathPolicyError> {
    let directory = File::open(path)
        .map_err(|source| PathPolicyError::io("open directory for synchronization", path, source))?;
    directory
        .sync_all()
        .map_err(|source| PathPolicyError::io("synchronize directory", path, source))
}

#[cfg(not(unix))]
pub fn sync_directory(_path: &Path) -> Result<(), PathPolicyError> {
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{PathPolicyError, prepare_destination, write_new_file};
    use crate::domain::LogicalPath;
    use std::fs;
    use std::path::PathBuf;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn temporary_directory(label: &str) -> PathBuf {
        let stamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("clock after epoch")
            .as_nanos();
        std::env::temp_dir().join(format!("framevault-{label}-{}-{stamp}", std::process::id()))
    }

    #[test]
    fn nested_file_is_created_without_overwrite() {
        let base = temporary_directory("extract");
        let logical = LogicalPath::parse("docs/guide.txt").expect("valid path");
        let destination = write_new_file(&base, &logical, b"guide").expect("write succeeds");
        assert_eq!(fs::read(&destination).expect("read output"), b"guide");
        assert!(matches!(
            prepare_destination(&base, &logical),
            Err(PathPolicyError::DestinationExists(_))
        ));
        fs::remove_dir_all(base).expect("remove fixture");
    }
}
