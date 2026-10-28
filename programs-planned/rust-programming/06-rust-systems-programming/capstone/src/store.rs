
//! File loading and same-directory transactional replacement.

use crate::aligned::{AlignedBytes, AllocationError};
use crate::codec::{DecodeError, EncodeError, Limits, decode, encode};
use crate::domain::Archive;
use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};

/// Evidence produced by one successful archive replacement.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SaveOutcome {
    /// The temporary file was flushed and synchronized before rename.
    pub file_synchronized: bool,
    /// The containing directory was synchronized after rename where supported.
    pub parent_directory_synchronized: bool,
}

/// A file-store failure that preserves its operational context.
#[derive(Debug)]
pub enum StoreError {
    Allocation(AllocationError),
    Encode(EncodeError),
    Decode(DecodeError),
    FileTooLarge { declared: u64, limit: usize },
    FileChangedWhileReading,
    TemporaryNameExhausted(PathBuf),
    ExistingReplacementUnsupported(PathBuf),
    CommittedButParentSyncFailed {
        path: PathBuf,
        source: io::Error,
    },
    Io {
        operation: &'static str,
        path: PathBuf,
        source: io::Error,
    },
}

impl StoreError {
    fn io(operation: &'static str, path: impl Into<PathBuf>, source: io::Error) -> Self {
        Self::Io {
            operation,
            path: path.into(),
            source,
        }
    }
}

impl fmt::Display for StoreError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Allocation(error) => write!(formatter, "allocation failed: {error}"),
            Self::Encode(error) => write!(formatter, "archive encoding failed: {error}"),
            Self::Decode(error) => write!(formatter, "archive decoding failed: {error}"),
            Self::FileTooLarge { declared, limit } => {
                write!(formatter, "file declares {declared} bytes, above limit {limit}")
            }
            Self::FileChangedWhileReading => formatter.write_str("archive changed while it was being read"),
            Self::TemporaryNameExhausted(path) => write!(formatter, "could not reserve a temporary name beside {}", path.display()),
            Self::ExistingReplacementUnsupported(path) => write!(
                formatter,
                "portable standard-library replacement of an existing destination is unsupported on this platform: {}",
                path.display()
            ),
            Self::CommittedButParentSyncFailed { path, source } => write!(
                formatter,
                "archive replacement at `{}` committed, but parent-directory synchronization failed: {source}",
                path.display()
            ),
            Self::Io { operation, path, source } => {
                write!(formatter, "could not {operation} `{}`: {source}", path.display())
            }
        }
    }
}

impl std::error::Error for StoreError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Allocation(error) => Some(error),
            Self::Encode(error) => Some(error),
            Self::Decode(error) => Some(error),
            Self::CommittedButParentSyncFailed { source, .. } | Self::Io { source, .. } => Some(source),
            _ => None,
        }
    }
}

impl From<AllocationError> for StoreError {
    fn from(error: AllocationError) -> Self {
        Self::Allocation(error)
    }
}

impl From<EncodeError> for StoreError {
    fn from(error: EncodeError) -> Self {
        Self::Encode(error)
    }
}

impl From<DecodeError> for StoreError {
    fn from(error: DecodeError) -> Self {
        Self::Decode(error)
    }
}

/// Read and decode an archive without first allocating from untrusted lengths.
pub fn load(path: &Path, limits: Limits) -> Result<Archive, StoreError> {
    let mut file = File::open(path).map_err(|source| StoreError::io("open archive", path, source))?;
    let declared = file
        .metadata()
        .map_err(|source| StoreError::io("read archive metadata", path, source))?
        .len();
    if declared > u64::try_from(limits.max_archive_bytes).unwrap_or(u64::MAX) {
        return Err(StoreError::FileTooLarge {
            declared,
            limit: limits.max_archive_bytes,
        });
    }
    let length = usize::try_from(declared).map_err(|_| StoreError::FileTooLarge {
        declared,
        limit: limits.max_archive_bytes,
    })?;

    let mut allocation = AlignedBytes::new_zeroed(length, 64)?;
    file.read_exact(allocation.as_mut_slice())
        .map_err(|source| StoreError::io("read archive", path, source))?;
    let mut probe = [0_u8; 1];
    if file
        .read(&mut probe)
        .map_err(|source| StoreError::io("check archive length", path, source))?
        != 0
    {
        return Err(StoreError::FileChangedWhileReading);
    }
    decode(allocation.as_slice(), limits).map_err(StoreError::from)
}

fn reserve_temporary(destination: &Path) -> Result<(PathBuf, File), StoreError> {
    let parent = destination
        .parent()
        .filter(|path| !path.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."));
    let name = destination
        .file_name()
        .and_then(|value| value.to_str())
        .unwrap_or("archive");

    for attempt in 0_u32..1024 {
        let candidate = parent.join(format!(
            ".{name}.framevault-tmp-{}-{attempt}",
            std::process::id()
        ));
        match OpenOptions::new().write(true).create_new(true).open(&candidate) {
            Ok(file) => return Ok((candidate, file)),
            Err(error) if error.kind() == io::ErrorKind::AlreadyExists => continue,
            Err(source) => return Err(StoreError::io("create temporary archive", candidate, source)),
        }
    }
    Err(StoreError::TemporaryNameExhausted(destination.to_path_buf()))
}

#[cfg(unix)]
fn replace(temporary: &Path, destination: &Path) -> Result<(), StoreError> {
    fs::rename(temporary, destination)
        .map_err(|source| StoreError::io("replace archive", destination, source))
}

#[cfg(not(unix))]
fn replace(temporary: &Path, destination: &Path) -> Result<(), StoreError> {
    if destination.exists() {
        return Err(StoreError::ExistingReplacementUnsupported(destination.to_path_buf()));
    }
    fs::rename(temporary, destination)
        .map_err(|source| StoreError::io("install archive", destination, source))
}

#[cfg(unix)]
fn synchronize_parent(parent: &Path) -> io::Result<bool> {
    let directory = File::open(parent)?;
    directory.sync_all()?;
    Ok(true)
}

#[cfg(not(unix))]
fn synchronize_parent(_parent: &Path) -> io::Result<bool> {
    Ok(false)
}


fn commit_candidate(
    mut file: File,
    temporary: &Path,
    destination: &Path,
    parent: &Path,
    bytes: &[u8],
) -> Result<SaveOutcome, StoreError> {
    file.write_all(bytes)
        .map_err(|source| StoreError::io("write temporary archive", temporary, source))?;
    file.flush()
        .map_err(|source| StoreError::io("flush temporary archive", temporary, source))?;
    file.sync_all()
        .map_err(|source| StoreError::io("synchronize temporary archive", temporary, source))?;
    drop(file);
    replace(temporary, destination)?;
    let parent_synchronized = synchronize_parent(parent).map_err(|source| {
        StoreError::CommittedButParentSyncFailed {
            path: destination.to_path_buf(),
            source,
        }
    })?;
    Ok(SaveOutcome {
        file_synchronized: true,
        parent_directory_synchronized: parent_synchronized,
    })
}

/// Encode, synchronize, and replace an archive using a temporary file in the
/// destination directory.
///
/// On Unix the standard-library rename operation replaces an existing path in
/// the same filesystem. On other platforms this implementation refuses to
/// overwrite an existing destination rather than pretending to provide an
/// atomic guarantee that the standard library cannot express portably.
pub fn save_atomic(
    path: &Path,
    archive: &Archive,
    limits: Limits,
) -> Result<SaveOutcome, StoreError> {
    let bytes = encode(archive, limits)?;
    let parent = path
        .parent()
        .filter(|candidate| !candidate.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."));
    fs::create_dir_all(parent)
        .map_err(|source| StoreError::io("create archive directory", parent, source))?;

    let (temporary, file) = reserve_temporary(path)?;
    let write_result = commit_candidate(file, &temporary, path, parent, &bytes);

    if write_result.is_err() {
        let _ = fs::remove_file(&temporary);
    }
    write_result
}

#[cfg(test)]
mod tests {
    use super::{load, save_atomic};
    use crate::codec::Limits;
    use crate::domain::{Archive, Entry, EntryKind, LogicalPath};
    use std::fs;
    use std::path::PathBuf;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn temporary_file(label: &str) -> PathBuf {
        let stamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("clock after epoch")
            .as_nanos();
        std::env::temp_dir()
            .join(format!("framevault-store-{}-{stamp}", std::process::id()))
            .join(label)
    }

    fn archive(payload: &[u8]) -> Archive {
        Archive::from_entries(vec![Entry::new(
            EntryKind::File,
            LogicalPath::parse("payload.bin").expect("valid path"),
            payload.to_vec(),
        )])
        .expect("unique fixture")
    }

    #[test]
    fn saved_archive_can_be_loaded() {
        let path = temporary_file("archive.fv");
        let expected = archive(b"first");
        save_atomic(&path, &expected, Limits::default()).expect("save succeeds");
        assert_eq!(load(&path, Limits::default()).expect("load succeeds"), expected);
        fs::remove_dir_all(path.parent().expect("fixture parent")).expect("remove fixture");
    }

    #[cfg(unix)]
    #[test]
    fn replacement_changes_the_complete_archive() {
        let path = temporary_file("replace.fv");
        save_atomic(&path, &archive(b"old"), Limits::default()).expect("first save");
        let newer = archive(b"new");
        save_atomic(&path, &newer, Limits::default()).expect("replacement save");
        assert_eq!(load(&path, Limits::default()).expect("load replacement"), newer);
        fs::remove_dir_all(path.parent().expect("fixture parent")).expect("remove fixture");
    }
}
