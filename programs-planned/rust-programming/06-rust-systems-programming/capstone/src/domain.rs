
//! Domain values whose invariants are independent of files and FFI.

use std::collections::HashSet;
use std::fmt;

/// The semantic kind of one archive entry.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum EntryKind {
    /// A regular file payload that may be extracted.
    File = 1,
    /// A structured process-capture payload.
    CommandCapture = 2,
}

impl EntryKind {
    /// Decode the stable wire code.
    #[must_use]
    pub const fn from_code(code: u8) -> Option<Self> {
        match code {
            1 => Some(Self::File),
            2 => Some(Self::CommandCapture),
            _ => None,
        }
    }

    /// Return the stable wire code.
    #[must_use]
    pub const fn code(self) -> u8 {
        self as u8
    }

    /// Return a stable display name.
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::File => "file",
            Self::CommandCapture => "command",
        }
    }
}

/// A normalized, portable archive path.
///
/// The representation uses `/` separators, is always relative, and contains
/// no empty, current-directory, parent-directory, drive-prefix, NUL, or
/// control-character component.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct LogicalPath(String);

impl LogicalPath {
    /// Validate and construct a logical path.
    pub fn parse(value: &str) -> Result<Self, LogicalPathError> {
        if value.is_empty() {
            return Err(LogicalPathError::Empty);
        }
        if value.starts_with('/') || value.starts_with('\\') {
            return Err(LogicalPathError::Absolute);
        }
        if value.contains('\\') {
            return Err(LogicalPathError::Backslash);
        }
        if value.contains(':') {
            return Err(LogicalPathError::DriveOrSchemeMarker);
        }
        if value.chars().any(|ch| ch == '\0' || ch.is_control()) {
            return Err(LogicalPathError::ControlCharacter);
        }

        for component in value.split('/') {
            match component {
                "" => return Err(LogicalPathError::EmptyComponent),
                "." => return Err(LogicalPathError::CurrentDirectory),
                ".." => return Err(LogicalPathError::ParentDirectory),
                _ => {}
            }
        }

        Ok(Self(value.to_owned()))
    }

    /// Borrow the portable path text.
    #[must_use]
    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// Iterate over validated path components.
    pub fn components(&self) -> impl Iterator<Item = &str> {
        self.0.split('/')
    }
}

impl fmt::Display for LogicalPath {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_str())
    }
}

/// Why text could not become a portable logical path.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogicalPathError {
    Empty,
    Absolute,
    Backslash,
    DriveOrSchemeMarker,
    ControlCharacter,
    EmptyComponent,
    CurrentDirectory,
    ParentDirectory,
}

impl fmt::Display for LogicalPathError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::Empty => "logical path is empty",
            Self::Absolute => "logical path is absolute",
            Self::Backslash => "logical path contains a backslash",
            Self::DriveOrSchemeMarker => "logical path contains a drive or scheme marker",
            Self::ControlCharacter => "logical path contains a NUL or control character",
            Self::EmptyComponent => "logical path contains an empty component",
            Self::CurrentDirectory => "logical path contains a current-directory component",
            Self::ParentDirectory => "logical path contains a parent-directory component",
        };
        formatter.write_str(message)
    }
}

impl std::error::Error for LogicalPathError {}

/// One owned archive entry.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    kind: EntryKind,
    name: LogicalPath,
    payload: Vec<u8>,
}

impl Entry {
    /// Construct one validated entry.
    #[must_use]
    pub fn new(kind: EntryKind, name: LogicalPath, payload: Vec<u8>) -> Self {
        Self {
            kind,
            name,
            payload,
        }
    }

    #[must_use]
    pub const fn kind(&self) -> EntryKind {
        self.kind
    }

    #[must_use]
    pub fn name(&self) -> &LogicalPath {
        &self.name
    }

    #[must_use]
    pub fn payload(&self) -> &[u8] {
        &self.payload
    }

    #[must_use]
    pub fn payload_len(&self) -> usize {
        self.payload.len()
    }
}

/// A validated collection of uniquely named entries.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct Archive {
    entries: Vec<Entry>,
}

impl Archive {
    #[must_use]
    pub const fn new() -> Self {
        Self { entries: Vec::new() }
    }

    /// Construct an archive and reject duplicate logical names.
    pub fn from_entries(entries: Vec<Entry>) -> Result<Self, ArchiveError> {
        let mut names = HashSet::with_capacity(entries.len());
        for entry in &entries {
            if !names.insert(entry.name().as_str()) {
                return Err(ArchiveError::DuplicateName(entry.name().clone()));
            }
        }
        Ok(Self { entries })
    }

    /// Insert one entry while preserving the unique-name invariant.
    pub fn push(&mut self, entry: Entry) -> Result<(), ArchiveError> {
        if self.entries.iter().any(|existing| existing.name() == entry.name()) {
            return Err(ArchiveError::DuplicateName(entry.name().clone()));
        }
        self.entries.push(entry);
        Ok(())
    }

    #[must_use]
    pub fn entries(&self) -> &[Entry] {
        &self.entries
    }

    #[must_use]
    pub fn entry_count(&self) -> usize {
        self.entries.len()
    }

    #[must_use]
    pub fn total_payload_bytes(&self) -> u64 {
        self.entries.iter().fold(0_u64, |total, entry| {
            total.saturating_add(u64::try_from(entry.payload_len()).unwrap_or(u64::MAX))
        })
    }
}

/// A domain-level archive invariant failure.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ArchiveError {
    DuplicateName(LogicalPath),
}

impl fmt::Display for ArchiveError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DuplicateName(name) => write!(formatter, "duplicate archive entry name `{name}`"),
        }
    }
}

impl std::error::Error for ArchiveError {}

#[cfg(test)]
mod tests {
    use super::{Archive, Entry, EntryKind, LogicalPath, LogicalPathError};

    #[test]
    fn logical_paths_reject_escape_syntax() {
        assert_eq!(LogicalPath::parse("../secret"), Err(LogicalPathError::ParentDirectory));
        assert_eq!(LogicalPath::parse("a//b"), Err(LogicalPathError::EmptyComponent));
        assert_eq!(LogicalPath::parse("C:/data"), Err(LogicalPathError::DriveOrSchemeMarker));
    }

    #[test]
    fn archive_rejects_duplicate_names() {
        let name = LogicalPath::parse("docs/readme.txt").expect("valid fixture path");
        let entries = vec![
            Entry::new(EntryKind::File, name.clone(), b"one".to_vec()),
            Entry::new(EntryKind::File, name, b"two".to_vec()),
        ];
        assert!(Archive::from_entries(entries).is_err());
    }
}
