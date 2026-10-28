
#![forbid(unsafe_code)]

use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Write};
use std::path::{Path, PathBuf};

#[derive(Debug)]
pub enum StoreError {
    CreateParent {
        path: PathBuf,
        source: io::Error,
    },
    CreateTemp {
        path: PathBuf,
        source: io::Error,
    },
    ExhaustedTempNames {
        destination: PathBuf,
    },
    WriteTemp {
        path: PathBuf,
        source: io::Error,
    },
    FlushTemp {
        path: PathBuf,
        source: io::Error,
    },
    SyncTemp {
        path: PathBuf,
        source: io::Error,
    },
    Replace {
        from: PathBuf,
        to: PathBuf,
        source: io::Error,
    },
    CommittedButParentSyncFailed {
        destination: PathBuf,
        parent: PathBuf,
        source: io::Error,
    },
    ExistingReplacementUnsupported {
        destination: PathBuf,
    },
}

impl fmt::Display for StoreError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::CreateParent { path, source } => {
                write!(formatter, "could not create parent `{}`: {source}", path.display())
            }
            Self::CreateTemp { path, source } => {
                write!(formatter, "could not create temporary file `{}`: {source}", path.display())
            }
            Self::ExhaustedTempNames { destination } => write!(
                formatter,
                "could not reserve a temporary sibling for `{}`",
                destination.display()
            ),
            Self::WriteTemp { path, source } => {
                write!(formatter, "could not write temporary file `{}`: {source}", path.display())
            }
            Self::FlushTemp { path, source } => {
                write!(formatter, "could not flush temporary file `{}`: {source}", path.display())
            }
            Self::SyncTemp { path, source } => write!(
                formatter,
                "could not synchronize temporary file `{}`: {source}",
                path.display()
            ),
            Self::Replace { from, to, source } => write!(
                formatter,
                "could not replace `{}` with `{}`: {source}",
                to.display(),
                from.display()
            ),
            Self::CommittedButParentSyncFailed {
                destination,
                parent,
                source,
            } => write!(
                formatter,
                "replacement at `{}` committed, but parent `{}` could not be synchronized: {source}",
                destination.display(),
                parent.display()
            ),
            Self::ExistingReplacementUnsupported { destination } => write!(
                formatter,
                "portable replacement of existing `{}` is unsupported on this target",
                destination.display()
            ),
        }
    }
}

impl std::error::Error for StoreError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::CreateParent { source, .. }
            | Self::CreateTemp { source, .. }
            | Self::WriteTemp { source, .. }
            | Self::FlushTemp { source, .. }
            | Self::SyncTemp { source, .. }
            | Self::Replace { source, .. }
            | Self::CommittedButParentSyncFailed { source, .. } => Some(source),
            Self::ExhaustedTempNames { .. }
            | Self::ExistingReplacementUnsupported { .. } => None,
        }
    }
}

#[must_use]
pub fn candidate_name(destination: &Path, attempt: u32) -> PathBuf {
    let file = destination
        .file_name()
        .unwrap_or_default()
        .to_string_lossy();
    destination.with_file_name(format!(
        ".{file}.{}.{}.tmp",
        std::process::id(),
        attempt
    ))
}

fn create_temp(destination: &Path) -> Result<(PathBuf, File), StoreError> {
    for attempt in 0..64 {
        let path = candidate_name(destination, attempt);
        match OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&path)
        {
            Ok(file) => return Ok((path, file)),
            Err(error) if error.kind() == io::ErrorKind::AlreadyExists => continue,
            Err(source) => return Err(StoreError::CreateTemp { path, source }),
        }
    }
    Err(StoreError::ExhaustedTempNames {
        destination: destination.to_path_buf(),
    })
}

#[cfg(unix)]
fn install(temporary: &Path, destination: &Path) -> Result<(), StoreError> {
    fs::rename(temporary, destination).map_err(|source| StoreError::Replace {
        from: temporary.to_path_buf(),
        to: destination.to_path_buf(),
        source,
    })
}

#[cfg(not(unix))]
fn install(temporary: &Path, destination: &Path) -> Result<(), StoreError> {
    if destination.exists() {
        return Err(StoreError::ExistingReplacementUnsupported {
            destination: destination.to_path_buf(),
        });
    }
    fs::rename(temporary, destination).map_err(|source| StoreError::Replace {
        from: temporary.to_path_buf(),
        to: destination.to_path_buf(),
        source,
    })
}

#[cfg(unix)]
fn sync_parent(parent: &Path) -> io::Result<()> {
    let directory = File::open(parent)?;
    directory.sync_all()
}

#[cfg(not(unix))]
fn sync_parent(_parent: &Path) -> io::Result<()> {
    Ok(())
}


fn commit_temporary(
    mut temporary: File,
    temporary_path: &Path,
    destination: &Path,
    parent: &Path,
    bytes: &[u8],
) -> Result<(), StoreError> {
    temporary
        .write_all(bytes)
        .map_err(|source| StoreError::WriteTemp {
            path: temporary_path.to_path_buf(),
            source,
        })?;
    temporary
        .flush()
        .map_err(|source| StoreError::FlushTemp {
            path: temporary_path.to_path_buf(),
            source,
        })?;
    temporary
        .sync_all()
        .map_err(|source| StoreError::SyncTemp {
            path: temporary_path.to_path_buf(),
            source,
        })?;
    drop(temporary);
    install(temporary_path, destination)?;
    sync_parent(parent).map_err(|source| StoreError::CommittedButParentSyncFailed {
        destination: destination.to_path_buf(),
        parent: parent.to_path_buf(),
        source,
    })
}

pub fn replace_bytes(destination: &Path, bytes: &[u8]) -> Result<(), StoreError> {
    let parent = destination
        .parent()
        .filter(|path| !path.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."));
    fs::create_dir_all(parent).map_err(|source| StoreError::CreateParent {
        path: parent.to_path_buf(),
        source,
    })?;

    let (temporary_path, temporary) = create_temp(destination)?;
    let outcome = commit_temporary(temporary, &temporary_path, destination, parent, bytes);

    if outcome.is_err() {
        let _ = fs::remove_file(&temporary_path);
    }
    outcome
}

#[cfg(test)]
mod tests {
    use super::replace_bytes;
    use std::fs;
    use std::path::PathBuf;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn fresh_dir(label: &str) -> PathBuf {
        let stamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("clock after epoch")
            .as_nanos();
        let path = std::env::temp_dir().join(format!(
            "course6-store-{label}-{}-{stamp}",
            std::process::id()
        ));
        fs::create_dir(&path).expect("create fixture");
        path
    }

    #[test]
    fn creates_a_new_value() {
        let directory = fresh_dir("new");
        let file = directory.join("state.bin");
        replace_bytes(&file, b"new").expect("save succeeds");
        assert_eq!(fs::read(&file).expect("read saved file"), b"new");
        fs::remove_dir_all(directory).expect("remove fixture");
    }

    #[cfg(unix)]
    #[test]
    fn replaces_an_existing_complete_value() {
        let directory = fresh_dir("replace");
        let file = directory.join("state.bin");
        fs::write(&file, b"old").expect("write old state");
        replace_bytes(&file, b"new").expect("replacement succeeds");
        assert_eq!(fs::read(&file).expect("read new state"), b"new");
        fs::remove_dir_all(directory).expect("remove fixture");
    }
}
