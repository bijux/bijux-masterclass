
//! Safe encoding and checked decoding for the `FRMVLT01` archive format.

use crate::checksum::checksum32;
use crate::domain::{Archive, ArchiveError, Entry, EntryKind, LogicalPath, LogicalPathError};
use std::collections::HashSet;
use std::fmt;

const MAGIC: &[u8; 8] = b"FRMVLT01";
const HEADER_SIZE: usize = 16;
const ENTRY_HEADER_SIZE: usize = 20;

/// Defensive limits applied before allocation and copying.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Limits {
    pub max_archive_bytes: usize,
    pub max_entries: usize,
    pub max_name_bytes: usize,
    pub max_payload_bytes: usize,
    pub max_total_payload_bytes: usize,
}

impl Default for Limits {
    fn default() -> Self {
        Self {
            max_archive_bytes: 64 * 1024 * 1024,
            max_entries: 10_000,
            max_name_bytes: 4 * 1024,
            max_payload_bytes: 32 * 1024 * 1024,
            max_total_payload_bytes: 48 * 1024 * 1024,
        }
    }
}

/// A failure to represent a valid archive in the wire format.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EncodeError {
    TooManyEntries,
    NameTooLong { name: String },
    PayloadTooLong { name: String },
    ArchiveTooLarge,
    SizeOverflow,
}

impl fmt::Display for EncodeError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::TooManyEntries => formatter.write_str("entry count does not fit the wire format"),
            Self::NameTooLong { name } => write!(formatter, "entry name is too long: `{name}`"),
            Self::PayloadTooLong { name } => write!(formatter, "entry payload is too long: `{name}`"),
            Self::ArchiveTooLarge => formatter.write_str("encoded archive exceeds the configured limit"),
            Self::SizeOverflow => formatter.write_str("encoded archive size overflowed"),
        }
    }
}

impl std::error::Error for EncodeError {}

/// A decoding failure with the byte offset at which it was detected.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DecodeError {
    offset: usize,
    kind: DecodeErrorKind,
}

impl DecodeError {
    #[must_use]
    pub const fn offset(&self) -> usize {
        self.offset
    }

    #[must_use]
    pub const fn kind(&self) -> &DecodeErrorKind {
        &self.kind
    }
}

/// The causal category of a decoding failure.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DecodeErrorKind {
    ArchiveTooLarge,
    Truncated { needed: usize, remaining: usize },
    InvalidMagic,
    NonZeroHeaderReserved,
    TooManyEntries { declared: usize },
    UnknownEntryKind { code: u8 },
    UnsupportedFlags { flags: u8 },
    NonZeroEntryReserved,
    NameTooLong { declared: usize },
    PayloadTooLong { declared: usize },
    TotalPayloadTooLong,
    InvalidUtf8Name,
    InvalidLogicalPath(LogicalPathError),
    DuplicateName(String),
    ChecksumMismatch { expected: u32, actual: u32 },
    TrailingBytes { count: usize },
    NumericOverflow,
}

impl fmt::Display for DecodeError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "archive decode error at byte {}: ", self.offset)?;
        match &self.kind {
            DecodeErrorKind::ArchiveTooLarge => formatter.write_str("input exceeds the configured archive limit"),
            DecodeErrorKind::Truncated { needed, remaining } => {
                write!(formatter, "needed {needed} bytes but only {remaining} remain")
            }
            DecodeErrorKind::InvalidMagic => formatter.write_str("invalid magic/version header"),
            DecodeErrorKind::NonZeroHeaderReserved => formatter.write_str("header reserved field is non-zero"),
            DecodeErrorKind::TooManyEntries { declared } => {
                write!(formatter, "declared entry count {declared} exceeds the configured limit")
            }
            DecodeErrorKind::UnknownEntryKind { code } => write!(formatter, "unknown entry kind {code}"),
            DecodeErrorKind::UnsupportedFlags { flags } => write!(formatter, "unsupported entry flags 0x{flags:02x}"),
            DecodeErrorKind::NonZeroEntryReserved => formatter.write_str("entry reserved field is non-zero"),
            DecodeErrorKind::NameTooLong { declared } => write!(formatter, "declared name length {declared} is too large"),
            DecodeErrorKind::PayloadTooLong { declared } => write!(formatter, "declared payload length {declared} is too large"),
            DecodeErrorKind::TotalPayloadTooLong => formatter.write_str("cumulative payload length exceeds the configured limit"),
            DecodeErrorKind::InvalidUtf8Name => formatter.write_str("entry name is not UTF-8"),
            DecodeErrorKind::InvalidLogicalPath(error) => write!(formatter, "invalid logical path: {error}"),
            DecodeErrorKind::DuplicateName(name) => write!(formatter, "duplicate entry name `{name}`"),
            DecodeErrorKind::ChecksumMismatch { expected, actual } => {
                write!(formatter, "payload checksum mismatch: expected {expected:#010x}, got {actual:#010x}")
            }
            DecodeErrorKind::TrailingBytes { count } => write!(formatter, "{count} trailing bytes remain"),
            DecodeErrorKind::NumericOverflow => formatter.write_str("wire value does not fit the host integer type"),
        }
    }
}

impl std::error::Error for DecodeError {}

fn decode_error(offset: usize, kind: DecodeErrorKind) -> DecodeError {
    DecodeError { offset, kind }
}

struct Cursor<'a> {
    bytes: &'a [u8],
    position: usize,
}

impl<'a> Cursor<'a> {
    const fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, position: 0 }
    }

    const fn position(&self) -> usize {
        self.position
    }

    fn remaining(&self) -> usize {
        self.bytes.len().saturating_sub(self.position)
    }

    fn take(&mut self, length: usize) -> Result<&'a [u8], DecodeError> {
        let end = self
            .position
            .checked_add(length)
            .ok_or_else(|| decode_error(self.position, DecodeErrorKind::NumericOverflow))?;
        if end > self.bytes.len() {
            return Err(decode_error(
                self.position,
                DecodeErrorKind::Truncated {
                    needed: length,
                    remaining: self.remaining(),
                },
            ));
        }
        let start = self.position;
        self.position = end;
        Ok(&self.bytes[start..end])
    }

    fn read_u8(&mut self) -> Result<u8, DecodeError> {
        Ok(self.take(1)?[0])
    }

    fn read_u16(&mut self) -> Result<u16, DecodeError> {
        let bytes = self.take(2)?;
        Ok(u16::from_le_bytes([bytes[0], bytes[1]]))
    }

    fn read_u32(&mut self) -> Result<u32, DecodeError> {
        let bytes = self.take(4)?;
        Ok(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }

    fn read_u64(&mut self) -> Result<u64, DecodeError> {
        let bytes = self.take(8)?;
        Ok(u64::from_le_bytes([
            bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7],
        ]))
    }
}

/// Encode a validated archive using the stable version-one format.
pub fn encode(archive: &Archive, limits: Limits) -> Result<Vec<u8>, EncodeError> {
    if archive.entry_count() > limits.max_entries {
        return Err(EncodeError::TooManyEntries);
    }
    let entry_count = u32::try_from(archive.entry_count()).map_err(|_| EncodeError::TooManyEntries)?;

    let mut required = HEADER_SIZE;
    let mut total_payload = 0_usize;
    for entry in archive.entries() {
        let name_length = entry.name().as_str().len();
        if name_length > limits.max_name_bytes || u16::try_from(name_length).is_err() {
            return Err(EncodeError::NameTooLong {
                name: entry.name().as_str().to_owned(),
            });
        }
        if entry.payload_len() > limits.max_payload_bytes || u64::try_from(entry.payload_len()).is_err() {
            return Err(EncodeError::PayloadTooLong {
                name: entry.name().as_str().to_owned(),
            });
        }
        total_payload = total_payload
            .checked_add(entry.payload_len())
            .ok_or(EncodeError::SizeOverflow)?;
        if total_payload > limits.max_total_payload_bytes {
            return Err(EncodeError::ArchiveTooLarge);
        }
        required = required
            .checked_add(ENTRY_HEADER_SIZE)
            .and_then(|value| value.checked_add(name_length))
            .and_then(|value| value.checked_add(entry.payload_len()))
            .ok_or(EncodeError::SizeOverflow)?;
    }
    if required > limits.max_archive_bytes {
        return Err(EncodeError::ArchiveTooLarge);
    }

    let mut output = Vec::new();
    output.try_reserve_exact(required).map_err(|_| EncodeError::ArchiveTooLarge)?;
    output.extend_from_slice(MAGIC);
    output.extend_from_slice(&entry_count.to_le_bytes());
    output.extend_from_slice(&0_u32.to_le_bytes());

    for entry in archive.entries() {
        let name = entry.name().as_str().as_bytes();
        let name_length = u16::try_from(name.len()).map_err(|_| EncodeError::NameTooLong {
            name: entry.name().as_str().to_owned(),
        })?;
        let payload_length = u64::try_from(entry.payload_len()).map_err(|_| EncodeError::PayloadTooLong {
            name: entry.name().as_str().to_owned(),
        })?;

        output.push(entry.kind().code());
        output.push(0);
        output.extend_from_slice(&name_length.to_le_bytes());
        output.extend_from_slice(&payload_length.to_le_bytes());
        output.extend_from_slice(&checksum32(entry.payload()).to_le_bytes());
        output.extend_from_slice(&0_u32.to_le_bytes());
        output.extend_from_slice(name);
        output.extend_from_slice(entry.payload());
    }

    Ok(output)
}

/// Decode one complete archive while enforcing all supplied limits.
pub fn decode(input: &[u8], limits: Limits) -> Result<Archive, DecodeError> {
    if input.len() > limits.max_archive_bytes {
        return Err(decode_error(0, DecodeErrorKind::ArchiveTooLarge));
    }

    let mut cursor = Cursor::new(input);
    if cursor.take(MAGIC.len())? != MAGIC {
        return Err(decode_error(0, DecodeErrorKind::InvalidMagic));
    }
    let declared_entries = usize::try_from(cursor.read_u32()?)
        .map_err(|_| decode_error(cursor.position(), DecodeErrorKind::NumericOverflow))?;
    let header_reserved_offset = cursor.position();
    if cursor.read_u32()? != 0 {
        return Err(decode_error(
            header_reserved_offset,
            DecodeErrorKind::NonZeroHeaderReserved,
        ));
    }
    if declared_entries > limits.max_entries {
        return Err(decode_error(
            8,
            DecodeErrorKind::TooManyEntries {
                declared: declared_entries,
            },
        ));
    }

    let mut entries = Vec::new();
    entries
        .try_reserve_exact(declared_entries)
        .map_err(|_| decode_error(cursor.position(), DecodeErrorKind::ArchiveTooLarge))?;
    let mut total_payload = 0_usize;
    let mut seen_names = HashSet::with_capacity(declared_entries);

    for _ in 0..declared_entries {
        let entry_start = cursor.position();
        let kind_code = cursor.read_u8()?;
        let kind = EntryKind::from_code(kind_code).ok_or_else(|| {
            decode_error(
                entry_start,
                DecodeErrorKind::UnknownEntryKind { code: kind_code },
            )
        })?;
        let flags_offset = cursor.position();
        let flags = cursor.read_u8()?;
        if flags != 0 {
            return Err(decode_error(
                flags_offset,
                DecodeErrorKind::UnsupportedFlags { flags },
            ));
        }
        let name_length_offset = cursor.position();
        let name_length = usize::from(cursor.read_u16()?);
        if name_length > limits.max_name_bytes {
            return Err(decode_error(
                name_length_offset,
                DecodeErrorKind::NameTooLong {
                    declared: name_length,
                },
            ));
        }
        let payload_length_offset = cursor.position();
        let payload_length_u64 = cursor.read_u64()?;
        let payload_length = usize::try_from(payload_length_u64).map_err(|_| {
            decode_error(payload_length_offset, DecodeErrorKind::NumericOverflow)
        })?;
        if payload_length > limits.max_payload_bytes {
            return Err(decode_error(
                payload_length_offset,
                DecodeErrorKind::PayloadTooLong {
                    declared: payload_length,
                },
            ));
        }
        total_payload = total_payload
            .checked_add(payload_length)
            .ok_or_else(|| decode_error(payload_length_offset, DecodeErrorKind::NumericOverflow))?;
        if total_payload > limits.max_total_payload_bytes {
            return Err(decode_error(
                payload_length_offset,
                DecodeErrorKind::TotalPayloadTooLong,
            ));
        }

        let expected_checksum = cursor.read_u32()?;
        let reserved_offset = cursor.position();
        if cursor.read_u32()? != 0 {
            return Err(decode_error(
                reserved_offset,
                DecodeErrorKind::NonZeroEntryReserved,
            ));
        }

        let name_offset = cursor.position();
        let name_bytes = cursor.take(name_length)?;
        let name_text = std::str::from_utf8(name_bytes)
            .map_err(|_| decode_error(name_offset, DecodeErrorKind::InvalidUtf8Name))?;
        let logical_name = LogicalPath::parse(name_text).map_err(|error| {
            decode_error(name_offset, DecodeErrorKind::InvalidLogicalPath(error))
        })?;
        if !seen_names.insert(logical_name.clone()) {
            return Err(decode_error(
                name_offset,
                DecodeErrorKind::DuplicateName(logical_name.as_str().to_owned()),
            ));
        }

        let payload_offset = cursor.position();
        let payload = cursor.take(payload_length)?;
        let actual_checksum = checksum32(payload);
        if actual_checksum != expected_checksum {
            return Err(decode_error(
                payload_offset,
                DecodeErrorKind::ChecksumMismatch {
                    expected: expected_checksum,
                    actual: actual_checksum,
                },
            ));
        }

        entries.push(Entry::new(kind, logical_name, payload.to_vec()));
    }

    if cursor.remaining() != 0 {
        return Err(decode_error(
            cursor.position(),
            DecodeErrorKind::TrailingBytes {
                count: cursor.remaining(),
            },
        ));
    }

    Archive::from_entries(entries).map_err(|error| match error {
        ArchiveError::DuplicateName(name) => decode_error(
            0,
            DecodeErrorKind::DuplicateName(name.as_str().to_owned()),
        ),
    })
}

#[cfg(test)]
mod tests {
    use super::{DecodeErrorKind, Limits, decode, encode};
    use crate::domain::{Archive, Entry, EntryKind, LogicalPath};

    fn sample_archive() -> Archive {
        Archive::from_entries(vec![Entry::new(
            EntryKind::File,
            LogicalPath::parse("docs/readme.txt").expect("valid fixture path"),
            b"systems course".to_vec(),
        )])
        .expect("unique fixture")
    }

    #[test]
    fn round_trip_preserves_domain_values() {
        let archive = sample_archive();
        let bytes = encode(&archive, Limits::default()).expect("encodable fixture");
        assert_eq!(decode(&bytes, Limits::default()), Ok(archive));
    }

    #[test]
    fn truncation_reports_the_detection_offset() {
        let bytes = encode(&sample_archive(), Limits::default()).expect("encodable fixture");
        let error = decode(&bytes[..bytes.len() - 1], Limits::default())
            .expect_err("truncated input must fail");
        assert!(matches!(error.kind(), DecodeErrorKind::Truncated { .. }));
    }

    #[test]
    fn checksum_corruption_is_not_silently_accepted() {
        let mut bytes = encode(&sample_archive(), Limits::default()).expect("encodable fixture");
        let last = bytes.len() - 1;
        bytes[last] ^= 0x40;
        let error = decode(&bytes, Limits::default()).expect_err("corruption must fail");
        assert!(matches!(error.kind(), DecodeErrorKind::ChecksumMismatch { .. }));
    }
}
