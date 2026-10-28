use crate::{DomainError, Item, ItemId, ItemState, Ledger};
use std::collections::HashSet;
use std::error::Error;
use std::ffi::OsString;
use std::fmt;
use std::fs::{self, File, OpenOptions};
use std::io::{self, BufRead, BufReader, Write};
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

const HEADER: &str = "INVENTORY-LEDGER-V1";

/// Failure while decoding one item record.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RecordError {
    /// Expected five tab-separated fields.
    WrongFieldCount,
    /// Record tag was not `ITEM`.
    WrongTag(String),
    /// Item ID was invalid.
    InvalidId(String),
    /// State label was invalid.
    InvalidState(String),
    /// Borrower field contradicted state.
    InvalidBorrowerField,
    /// Restored domain value violated an invariant.
    InvalidDomain(String),
}

impl fmt::Display for RecordError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::WrongFieldCount => write!(
                formatter,
                "expected ITEM<TAB>ID<TAB>STATE<TAB>BORROWER<TAB>NAME"
            ),
            Self::WrongTag(value) => write!(formatter, "expected ITEM tag, found `{value}`"),
            Self::InvalidId(value) => write!(formatter, "invalid nonzero item ID `{value}`"),
            Self::InvalidState(value) => write!(formatter, "invalid item state `{value}`"),
            Self::InvalidBorrowerField => {
                write!(formatter, "borrower field does not match item state")
            }
            Self::InvalidDomain(value) => write!(formatter, "invalid restored item: {value}"),
        }
    }
}

impl Error for RecordError {}

/// Persistence failure with structural and path context.
#[derive(Debug)]
pub enum StorageError {
    /// Generic reader or writer failed.
    Io(io::Error),
    /// File operation failed with path context.
    PathIo {
        /// Operation attempted.
        operation: &'static str,
        /// Affected path.
        path: PathBuf,
        /// Underlying I/O failure.
        source: io::Error,
    },
    /// Header line was absent.
    MissingHeader,
    /// Header version was unsupported.
    InvalidHeader(String),
    /// Next-ID metadata was absent.
    MissingMetadata,
    /// Next-ID metadata was malformed.
    InvalidMetadata(String),
    /// One item record was malformed.
    InvalidRecord {
        /// One-based line number.
        line: usize,
        /// Structured record cause.
        source: RecordError,
    },
    /// Duplicate ID was found at a specific line.
    DuplicateId {
        /// One-based line number.
        line: usize,
        /// Repeated ID.
        id: ItemId,
    },
    /// Snapshot-level domain invariant failed.
    InvalidSnapshot(String),
    /// Target path had no file name for temporary replacement.
    InvalidTarget(PathBuf),
}

impl fmt::Display for StorageError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(formatter, "inventory codec I/O failed: {error}"),
            Self::PathIo {
                operation,
                path,
                source,
            } => write!(
                formatter,
                "could not {operation} `{}`: {source}",
                path.display()
            ),
            Self::MissingHeader => write!(formatter, "inventory header is missing"),
            Self::InvalidHeader(value) => {
                write!(formatter, "unsupported inventory header `{value}`")
            }
            Self::MissingMetadata => write!(formatter, "NEXT metadata is missing"),
            Self::InvalidMetadata(value) => write!(formatter, "invalid NEXT metadata: {value}"),
            Self::InvalidRecord { line, source } => {
                write!(formatter, "invalid inventory record at line {line}: {source}")
            }
            Self::DuplicateId { line, id } => {
                write!(formatter, "duplicate item ID {id} at line {line}")
            }
            Self::InvalidSnapshot(value) => {
                write!(formatter, "invalid inventory snapshot: {value}")
            }
            Self::InvalidTarget(path) => write!(
                formatter,
                "storage target `{}` has no file name",
                path.display()
            ),
        }
    }
}

impl Error for StorageError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
            Self::PathIo { source, .. } => Some(source),
            Self::InvalidRecord { source, .. } => Some(source),
            _ => None,
        }
    }
}

impl From<io::Error> for StorageError {
    fn from(error: io::Error) -> Self {
        Self::Io(error)
    }
}

/// Loads a complete snapshot from any buffered reader.
pub fn load_from<R: BufRead>(reader: R) -> Result<Ledger, StorageError> {
    let mut lines = reader.lines().enumerate();
    let header = match lines.next() {
        Some((_, line)) => line?,
        None => return Err(StorageError::MissingHeader),
    };
    if header != HEADER {
        return Err(StorageError::InvalidHeader(header));
    }
    let metadata = match lines.next() {
        Some((_, line)) => line?,
        None => return Err(StorageError::MissingMetadata),
    };
    let next_id = parse_metadata(&metadata)?;

    let mut items = Vec::new();
    let mut seen = HashSet::new();
    for (index, line) in lines {
        let line_number = index + 1;
        let line = line?;
        let item = decode_record(&line).map_err(|source| StorageError::InvalidRecord {
            line: line_number,
            source,
        })?;
        if !seen.insert(item.id()) {
            return Err(StorageError::DuplicateId {
                line: line_number,
                id: item.id(),
            });
        }
        items.push(item);
    }
    Ledger::restore(items, next_id)
        .map_err(|error| StorageError::InvalidSnapshot(error.to_string()))
}

/// Writes a deterministic ID-sorted snapshot to any writer.
pub fn save_to<W: Write>(writer: &mut W, ledger: &Ledger) -> Result<(), StorageError> {
    writeln!(writer, "{HEADER}")?;
    match ledger.next_id_token() {
        Some(value) => writeln!(writer, "NEXT\t{value}")?,
        None => writeln!(writer, "NEXT\texhausted")?,
    }
    let mut items: Vec<_> = ledger.items().iter().collect();
    items.sort_unstable_by_key(|item| item.id());
    for item in items {
        let (state, borrower) = match item.state() {
            ItemState::Available => ("available", ""),
            ItemState::CheckedOut { borrower } => ("checked-out", borrower.as_str()),
            ItemState::Retired => ("retired", ""),
        };
        writeln!(writer, "ITEM\t{}\t{state}\t{borrower}\t{}", item.id(), item.name())?;
    }
    Ok(())
}

/// Loads a path; absence means a new ledger, while every other failure is preserved.
pub fn load_path(path: &Path) -> Result<Ledger, StorageError> {
    match File::open(path) {
        Ok(file) => load_from(BufReader::new(file)),
        Err(error) if error.kind() == io::ErrorKind::NotFound => Ok(Ledger::new()),
        Err(source) => Err(StorageError::PathIo {
            operation: "open",
            path: path.to_path_buf(),
            source,
        }),
    }
}

/// Replaces a snapshot through a same-directory temporary file.
pub fn save_path(path: &Path, ledger: &Ledger) -> Result<(), StorageError> {
    let temporary = temporary_path(path)?;
    let result = (|| {
        let mut file = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&temporary)
            .map_err(|source| StorageError::PathIo {
                operation: "create temporary storage",
                path: temporary.clone(),
                source,
            })?;
        save_to(&mut file, ledger)?;
        file.sync_all().map_err(|source| StorageError::PathIo {
            operation: "synchronize temporary storage",
            path: temporary.clone(),
            source,
        })?;
        drop(file);
        fs::rename(&temporary, path).map_err(|source| StorageError::PathIo {
            operation: "replace storage",
            path: path.to_path_buf(),
            source,
        })?;
        Ok(())
    })();
    if result.is_err() {
        let _ignored = fs::remove_file(&temporary);
    }
    result
}

fn parse_metadata(line: &str) -> Result<Option<u64>, StorageError> {
    let mut fields = line.split('\t');
    if fields.next() != Some("NEXT") {
        return Err(StorageError::InvalidMetadata(String::from("expected NEXT tag")));
    }
    let Some(value) = fields.next() else {
        return Err(StorageError::InvalidMetadata(String::from("missing value")));
    };
    if fields.next().is_some() {
        return Err(StorageError::InvalidMetadata(String::from("unexpected extra fields")));
    }
    if value == "exhausted" {
        return Ok(None);
    }
    value
        .parse::<u64>()
        .ok()
        .filter(|value| *value != 0)
        .map(Some)
        .ok_or_else(|| {
            StorageError::InvalidMetadata(format!("invalid nonzero ID `{value}`"))
        })
}

fn decode_record(line: &str) -> Result<Item, RecordError> {
    let fields: Vec<_> = line.split('\t').collect();
    if fields.len() != 5 {
        return Err(RecordError::WrongFieldCount);
    }
    if fields[0] != "ITEM" {
        return Err(RecordError::WrongTag(fields[0].to_owned()));
    }
    let id = fields[1].parse::<ItemId>().map_err(|_| RecordError::InvalidId(fields[1].to_owned()))?;
    let state = match fields[2] {
        "available" if fields[3].is_empty() => ItemState::Available,
        "checked-out" if !fields[3].is_empty() => ItemState::CheckedOut {
            borrower: fields[3].to_owned(),
        },
        "retired" if fields[3].is_empty() => ItemState::Retired,
        "available" | "checked-out" | "retired" => return Err(RecordError::InvalidBorrowerField),
        other => return Err(RecordError::InvalidState(other.to_owned())),
    };
    Item::restore(id, fields[4].to_owned(), state)
        .map_err(|error| RecordError::InvalidDomain(error.to_string()))
}

fn temporary_path(path: &Path) -> Result<PathBuf, StorageError> {
    let Some(file_name) = path.file_name() else {
        return Err(StorageError::InvalidTarget(path.to_path_buf()));
    };
    let nonce = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_or(0, |duration| duration.as_nanos());
    let mut temporary_name = OsString::from(".");
    temporary_name.push(file_name);
    temporary_name.push(format!(".{}.{}.tmp", std::process::id(), nonce));
    Ok(path.with_file_name(temporary_name))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn codec_round_trip_is_deterministic_and_preserves_variant_data() {
        let mut ledger = Ledger::new();
        let caliper = ledger.add(String::from("Caliper")).expect("valid");
        ledger.add(String::from("Gauge")).expect("valid");
        ledger.checkout(caliper, String::from("Ada")).expect("available");
        let mut bytes = Vec::new();
        save_to(&mut bytes, &ledger).expect("memory write");
        let text = String::from_utf8(bytes.clone()).expect("UTF-8");
        assert_eq!(
            text,
            concat!(
                "INVENTORY-LEDGER-V1\n",
                "NEXT\t3\n",
                "ITEM\t1\tchecked-out\tAda\tCaliper\n",
                "ITEM\t2\tavailable\t\tGauge\n",
            )
        );
        assert_eq!(load_from(Cursor::new(bytes)).expect("round trip"), ledger);
    }

    #[test]
    fn hyphen_is_valid_borrower_data_not_a_persistence_sentinel() {
        let mut ledger = Ledger::new();
        let id = ledger.add(String::from("Caliper")).expect("valid");
        ledger
            .checkout(id, String::from("-"))
            .expect("available");

        let mut bytes = Vec::new();
        save_to(&mut bytes, &ledger).expect("memory write");
        assert_eq!(load_from(Cursor::new(bytes)).expect("round trip"), ledger);
    }

    #[test]
    fn malformed_borrower_state_is_rejected_at_record_line() {
        let input = "INVENTORY-LEDGER-V1\nNEXT\t2\nITEM\t1\tchecked-out\t\tCaliper\n";
        assert!(matches!(
            load_from(Cursor::new(input)),
            Err(StorageError::InvalidRecord {
                line: 3,
                source: RecordError::InvalidBorrowerField,
            })
        ));
    }

    #[test]
    fn inconsistent_metadata_is_not_silently_repaired() {
        let input = "INVENTORY-LEDGER-V1\nNEXT\t1\nITEM\t1\tavailable\t\tCaliper\n";
        assert!(matches!(load_from(Cursor::new(input)), Err(StorageError::InvalidSnapshot(_))));
    }
}
