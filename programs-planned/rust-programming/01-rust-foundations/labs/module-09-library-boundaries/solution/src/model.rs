//! Registry domain model and invariants.

use std::error::Error;
use std::fmt;
use std::str::FromStr;

/// Stable, nonzero identity assigned to one registry entry.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct EntryId(u64);

impl EntryId {
    /// Returns the numeric representation used for display and persistence.
    pub const fn get(self) -> u64 {
        self.0
    }
}

impl fmt::Display for EntryId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

/// The supplied text was not a valid nonzero [`EntryId`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseEntryIdError {
    input: String,
}

impl fmt::Display for ParseEntryIdError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "invalid nonzero entry ID `{}`", self.input)
    }
}

impl Error for ParseEntryIdError {}

impl FromStr for EntryId {
    type Err = ParseEntryIdError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        input
            .parse::<u64>()
            .ok()
            .filter(|value| *value != 0)
            .map(Self)
            .ok_or_else(|| ParseEntryIdError {
                input: input.to_owned(),
            })
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Entry {
    id: EntryId,
    label: String,
}

/// A read-only, borrowed projection of an internal entry.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EntryView<'a> {
    /// Stable entry identity.
    pub id: EntryId,
    /// Borrowed label owned by the registry.
    pub label: &'a str,
}

/// A domain rule rejected a requested registry operation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RegistryError {
    /// Labels must contain at least one non-whitespace character.
    EmptyLabel,
    /// Labels cannot contain storage delimiters or line boundaries.
    InvalidLabel,
    /// No further identifier can be represented by `u64`.
    IdExhausted,
    /// The requested entry is absent.
    NotFound(EntryId),
}

impl fmt::Display for RegistryError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyLabel => write!(formatter, "entry label cannot be empty"),
            Self::InvalidLabel => {
                write!(formatter, "entry label cannot contain line breaks or tabs")
            }
            Self::IdExhausted => write!(formatter, "entry ID space is exhausted"),
            Self::NotFound(id) => write!(formatter, "entry {id} was not found"),
        }
    }
}

impl Error for RegistryError {}

/// Ordered aggregate that owns entries and identifier allocation state.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Registry {
    entries: Vec<Entry>,
    next_id: Option<u64>,
}

impl Default for Registry {
    fn default() -> Self {
        Self::new()
    }
}

impl Registry {
    /// Constructs an empty registry whose first inserted entry receives ID 1.
    pub const fn new() -> Self {
        Self {
            entries: Vec::new(),
            next_id: Some(1),
        }
    }

    /// Validates and inserts one owned label, returning its fresh identity.
    pub fn add(&mut self, label: String) -> Result<EntryId, RegistryError> {
        let label = label.trim();
        if label.is_empty() {
            return Err(RegistryError::EmptyLabel);
        }
        if label
            .chars()
            .any(|character| matches!(character, '\t' | '\n' | '\r'))
        {
            return Err(RegistryError::InvalidLabel);
        }

        let raw = self.next_id.ok_or(RegistryError::IdExhausted)?;
        let id = EntryId(raw);
        self.next_id = raw.checked_add(1);
        self.entries.push(Entry {
            id,
            label: label.to_owned(),
        });
        Ok(id)
    }

    /// Borrows the entry with `id`, if present, without exposing storage fields.
    pub fn get(&self, id: EntryId) -> Option<EntryView<'_>> {
        self.entries
            .iter()
            .find(|entry| entry.id == id)
            .map(|entry| EntryView {
                id: entry.id,
                label: &entry.label,
            })
    }

    /// Removes an entry and returns ownership of its label.
    pub fn remove(&mut self, id: EntryId) -> Result<String, RegistryError> {
        let index = self
            .entries
            .iter()
            .position(|entry| entry.id == id)
            .ok_or(RegistryError::NotFound(id))?;
        Ok(self.entries.remove(index).label)
    }

    /// Iterates over borrowed read-only projections in insertion order.
    pub fn iter(&self) -> impl Iterator<Item = EntryView<'_>> {
        self.entries.iter().map(|entry| EntryView {
            id: entry.id,
            label: &entry.label,
        })
    }

    /// Returns the number of stored entries.
    pub fn len(&self) -> usize {
        self.entries.len()
    }

    /// Reports whether the registry contains no entries.
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parser_rejects_zero_and_non_numbers() {
        assert!("0".parse::<EntryId>().is_err());
        assert!("x".parse::<EntryId>().is_err());
        assert_eq!("9".parse::<EntryId>().map(EntryId::get), Ok(9));
    }

    #[test]
    fn removal_preserves_remaining_order_and_does_not_reuse_id() {
        let mut registry = Registry::new();
        let first = registry.add(String::from("first")).expect("valid");
        let second = registry.add(String::from("second")).expect("valid");
        registry.remove(first).expect("exists");
        let third = registry.add(String::from("third")).expect("valid");

        assert_eq!(third.get(), 3);
        assert_eq!(
            registry
                .iter()
                .map(|entry| (entry.id, entry.label))
                .collect::<Vec<_>>(),
            vec![(second, "second"), (third, "third")]
        );
    }
}
