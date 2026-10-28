//! Reference versioned inventory codec with contextual errors.

use std::collections::HashSet;
use std::error::Error;
use std::fmt;
use std::io::{self, BufRead, Write};
use std::str::FromStr;

const HEADER: &str = "INVENTORY-V1";
const MAX_TITLE_BYTES: usize = 120;

/// Nonzero item identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct ItemId(u64);

impl ItemId {
    /// Creates a nonzero ID.
    pub const fn new(value: u64) -> Option<Self> {
        if value == 0 {
            None
        } else {
            Some(Self(value))
        }
    }

    /// Returns the primitive value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for ItemId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

/// Persisted item state.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ItemState {
    /// Item can be checked out.
    Available,
    /// Item is currently checked out.
    CheckedOut,
}

impl fmt::Display for ItemState {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Available => "available",
            Self::CheckedOut => "checked-out",
        })
    }
}

/// Failure to parse an item-state label.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseItemStateError(String);

impl fmt::Display for ParseItemStateError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "unknown item state `{}`", self.0)
    }
}

impl Error for ParseItemStateError {}

impl FromStr for ItemState {
    type Err = ParseItemStateError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        match input {
            "available" => Ok(Self::Available),
            "checked-out" => Ok(Self::CheckedOut),
            other => Err(ParseItemStateError(other.to_owned())),
        }
    }
}

/// One persisted inventory item.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    id: ItemId,
    state: ItemState,
    title: String,
}

impl Item {
    /// Returns the stable ID.
    pub const fn id(&self) -> ItemId {
        self.id
    }

    /// Returns persisted state.
    pub const fn state(&self) -> ItemState {
        self.state
    }

    /// Borrows the title.
    pub fn title(&self) -> &str {
        &self.title
    }
}

/// Complete validated inventory snapshot.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Inventory {
    items: Vec<Item>,
    next_id: u64,
}

impl Inventory {
    /// Borrows restored items.
    pub fn items(&self) -> &[Item] {
        &self.items
    }

    /// Returns the next ID that would be allocated.
    pub const fn next_id(&self) -> u64 {
        self.next_id
    }
}

/// Failure while decoding one `ITEM` record.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RecordError {
    /// Record did not have exactly four fields.
    WrongFieldCount,
    /// First field was not `ITEM`.
    WrongTag(String),
    /// ID was not a nonzero unsigned integer.
    InvalidId(String),
    /// State label was unknown.
    InvalidState(String),
    /// Title was empty or exceeded the byte limit.
    InvalidTitle(String),
}

impl fmt::Display for RecordError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::WrongFieldCount => write!(formatter, "expected ITEM<TAB>ID<TAB>STATE<TAB>TITLE"),
            Self::WrongTag(tag) => write!(formatter, "expected ITEM tag, found `{tag}`"),
            Self::InvalidId(value) => write!(formatter, "invalid nonzero item ID `{value}`"),
            Self::InvalidState(value) => write!(formatter, "invalid item state `{value}`"),
            Self::InvalidTitle(reason) => write!(formatter, "invalid title: {reason}"),
        }
    }
}

impl Error for RecordError {}

/// Failure while loading or saving a complete inventory.
#[derive(Debug)]
pub enum StorageError {
    /// Underlying reader or writer failed.
    Io(io::Error),
    /// First line was absent.
    MissingHeader,
    /// First line was not the supported version.
    InvalidHeader(String),
    /// Metadata line was absent.
    MissingMetadata,
    /// Metadata line was malformed.
    InvalidMetadata {
        /// One-based line number.
        line: usize,
        /// Human-readable reason.
        message: String,
    },
    /// Item record was malformed.
    InvalidRecord {
        /// One-based line number.
        line: usize,
        /// Structured record cause.
        source: RecordError,
    },
    /// An ID occurred more than once.
    DuplicateId {
        /// Line containing the repeated ID.
        line: usize,
        /// Repeated ID.
        id: ItemId,
    },
    /// Metadata would permit ID reuse or used zero.
    InvalidNextId {
        /// Parsed next ID.
        next_id: u64,
        /// Largest restored ID, or zero for an empty inventory.
        maximum_id: u64,
    },
}

impl fmt::Display for StorageError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Io(error) => write!(formatter, "inventory I/O failed: {error}"),
            Self::MissingHeader => write!(formatter, "inventory header is missing"),
            Self::InvalidHeader(found) => {
                write!(formatter, "unsupported inventory header `{found}`")
            }
            Self::MissingMetadata => write!(formatter, "NEXT_ID metadata is missing"),
            Self::InvalidMetadata { line, message } => {
                write!(formatter, "invalid metadata at line {line}: {message}")
            }
            Self::InvalidRecord { line, source } => {
                write!(formatter, "invalid item at line {line}: {source}")
            }
            Self::DuplicateId { line, id } => {
                write!(formatter, "duplicate item ID {id} at line {line}")
            }
            Self::InvalidNextId { next_id, maximum_id } => {
                write!(
                    formatter,
                    concat!(
                        "NEXT_ID {next_id} must be nonzero and greater than ",
                        "maximum item ID {maximum_id}",
                    )
                )
            }
        }
    }
}

impl Error for StorageError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Io(error) => Some(error),
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

/// Decodes one item record without file or line-number concerns.
pub fn decode_item(line: &str) -> Result<Item, RecordError> {
    let fields: Vec<_> = line.split('\t').collect();
    if fields.len() != 4 {
        return Err(RecordError::WrongFieldCount);
    }
    if fields[0] != "ITEM" {
        return Err(RecordError::WrongTag(fields[0].to_owned()));
    }
    let raw_id = fields[1];
    let id = raw_id
        .parse::<u64>()
        .ok()
        .and_then(ItemId::new)
        .ok_or_else(|| RecordError::InvalidId(raw_id.to_owned()))?;
    let state = fields[2]
        .parse::<ItemState>()
        .map_err(|_| RecordError::InvalidState(fields[2].to_owned()))?;
    let title = fields[3];
    if title.trim().is_empty() {
        return Err(RecordError::InvalidTitle(String::from("title is empty")));
    }
    if title.len() > MAX_TITLE_BYTES {
        return Err(RecordError::InvalidTitle(format!(
            "{} bytes exceeds {MAX_TITLE_BYTES}",
            title.len()
        )));
    }
    Ok(Item {
        id,
        state,
        title: title.to_owned(),
    })
}

/// Loads and validates a complete inventory snapshot.
pub fn load_from<R: BufRead>(reader: R) -> Result<Inventory, StorageError> {
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
    let mut metadata_fields = metadata.split('\t');
    let tag = metadata_fields.next();
    let value = metadata_fields.next();
    if tag != Some("NEXT_ID") || value.is_none() || metadata_fields.next().is_some() {
        return Err(StorageError::InvalidMetadata {
            line: 2,
            message: String::from("expected NEXT_ID<TAB>unsigned-integer"),
        });
    }
    let raw_next_id = value.unwrap_or_default();
    let next_id = raw_next_id.parse::<u64>().map_err(|_| StorageError::InvalidMetadata {
        line: 2,
        message: format!("invalid unsigned integer `{raw_next_id}`"),
    })?;

    let mut seen = HashSet::new();
    let mut items = Vec::new();
    let mut maximum_id = 0_u64;
    for (index, line) in lines {
        let line_number = index + 1;
        let line = line?;
        let item = decode_item(&line).map_err(|source| StorageError::InvalidRecord {
            line: line_number,
            source,
        })?;
        if !seen.insert(item.id) {
            return Err(StorageError::DuplicateId { line: line_number, id: item.id });
        }
        maximum_id = maximum_id.max(item.id.get());
        items.push(item);
    }

    if next_id == 0 || next_id <= maximum_id {
        return Err(StorageError::InvalidNextId { next_id, maximum_id });
    }

    Ok(Inventory { items, next_id })
}

/// Writes a deterministic ID-sorted inventory snapshot.
pub fn save_to<W: Write>(writer: &mut W, inventory: &Inventory) -> Result<(), StorageError> {
    writeln!(writer, "{HEADER}")?;
    writeln!(writer, "NEXT_ID\t{}", inventory.next_id)?;
    let mut items: Vec<_> = inventory.items.iter().collect();
    items.sort_unstable_by_key(|item| item.id);
    for item in items {
        writeln!(writer, "ITEM\t{}\t{}\t{}", item.id, item.state, item.title)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::{Cursor, Read};

    #[test]
    fn valid_input_round_trips_deterministically() {
        let input = concat!(
            "INVENTORY-V1\n",
            "NEXT_ID\t3\n",
            "ITEM\t2\tchecked-out\tDrill\n",
            "ITEM\t1\tavailable\tHammer\n",
        );
        let inventory = load_from(Cursor::new(input)).expect("valid inventory");
        assert_eq!(inventory.next_id(), 3);
        let mut output = Vec::new();
        save_to(&mut output, &inventory).expect("memory write");
        assert_eq!(
            String::from_utf8(output).expect("valid UTF-8"),
            concat!(
                "INVENTORY-V1\n",
                "NEXT_ID\t3\n",
                "ITEM\t1\tavailable\tHammer\n",
                "ITEM\t2\tchecked-out\tDrill\n",
            )
        );
    }

    #[test]
    fn missing_and_invalid_headers_are_distinct() {
        assert!(matches!(load_from(Cursor::new("")), Err(StorageError::MissingHeader)));
        assert!(matches!(
            load_from(Cursor::new("OTHER\n")),
            Err(StorageError::InvalidHeader(found)) if found == "OTHER"
        ));
    }

    #[test]
    fn metadata_failures_are_contextual() {
        assert!(matches!(
            load_from(Cursor::new("INVENTORY-V1\n")),
            Err(StorageError::MissingMetadata)
        ));
        assert!(matches!(
            load_from(Cursor::new("INVENTORY-V1\nNEXT_ID\tbad\n")),
            Err(StorageError::InvalidMetadata { line: 2, .. })
        ));
    }

    #[test]
    fn record_failure_retains_line_and_source() {
        let error = load_from(Cursor::new(
            "INVENTORY-V1\nNEXT_ID\t2\nITEM\t0\tavailable\tBad\n",
        ))
        .expect_err("zero ID");
        assert!(matches!(
            error,
            StorageError::InvalidRecord {
                line: 3,
                source: RecordError::InvalidId(value),
            } if value == "0"
        ));
    }

    #[test]
    fn duplicate_and_next_id_invariants_are_distinct() {
        let duplicate = concat!(
            "INVENTORY-V1\n",
            "NEXT_ID\t3\n",
            "ITEM\t1\tavailable\tA\n",
            "ITEM\t1\tchecked-out\tB\n",
        );
        assert!(matches!(
            load_from(Cursor::new(duplicate)),
            Err(StorageError::DuplicateId { line: 4, id }) if id.get() == 1
        ));
        let reused = "INVENTORY-V1\nNEXT_ID\t2\nITEM\t2\tavailable\tA\n";
        assert!(matches!(
            load_from(Cursor::new(reused)),
            Err(StorageError::InvalidNextId {
                next_id: 2,
                maximum_id: 2,
            })
        ));
        assert!(matches!(
            load_from(Cursor::new("INVENTORY-V1\nNEXT_ID\t0\n")),
            Err(StorageError::InvalidNextId {
                next_id: 0,
                maximum_id: 0,
            })
        ));
    }

    struct ErrorReader;

    impl Read for ErrorReader {
        fn read(&mut self, _buffer: &mut [u8]) -> io::Result<usize> {
            Err(io::Error::other("synthetic read failure"))
        }
    }

    impl BufRead for ErrorReader {
        fn fill_buf(&mut self) -> io::Result<&[u8]> {
            Err(io::Error::other("synthetic read failure"))
        }

        fn consume(&mut self, _amount: usize) {}
    }

    #[test]
    fn io_failure_remains_a_source() {
        let error = load_from(ErrorReader).expect_err("reader fails");
        assert!(matches!(error, StorageError::Io(_)));
        assert!(error.source().is_some());
    }
}
