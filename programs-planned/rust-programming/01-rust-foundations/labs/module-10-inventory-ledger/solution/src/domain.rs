use std::collections::HashSet;
use std::error::Error;
use std::fmt;
use std::str::FromStr;

pub(crate) const MAX_NAME_BYTES: usize = 120;
pub(crate) const MAX_BORROWER_BYTES: usize = 80;

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

/// Failure to parse a nonzero item ID.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseItemIdError {
    input: String,
}

impl fmt::Display for ParseItemIdError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "invalid nonzero item ID `{}`", self.input)
    }
}

impl Error for ParseItemIdError {}

impl FromStr for ItemId {
    type Err = ParseItemIdError;

    fn from_str(input: &str) -> Result<Self, Self::Err> {
        input
            .parse::<u64>()
            .ok()
            .and_then(Self::new)
            .ok_or_else(|| ParseItemIdError {
                input: input.to_owned(),
            })
    }
}

/// Complete state of one item. Borrower data exists only in the checked-out variant.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ItemState {
    /// Item may be checked out or retired.
    Available,
    /// Item is held by a named borrower.
    CheckedOut {
        /// Person or team responsible for the item.
        borrower: String,
    },
    /// Item is permanently unavailable.
    Retired,
}

impl ItemState {
    pub(crate) const fn tag(&self) -> &'static str {
        match self {
            Self::Available => "available",
            Self::CheckedOut { .. } => "checked-out",
            Self::Retired => "retired",
        }
    }
}

/// One ledger-owned item.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Item {
    id: ItemId,
    name: String,
    state: ItemState,
}

impl Item {
    pub(crate) fn restore(id: ItemId, name: String, state: ItemState) -> Result<Self, DomainError> {
        validate_name(&name)?;
        if let ItemState::CheckedOut { borrower } = &state {
            validate_borrower(borrower)?;
        }
        Ok(Self { id, name, state })
    }

    /// Returns the stable identifier.
    pub const fn id(&self) -> ItemId {
        self.id
    }

    /// Borrows the item name.
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Borrows complete state, including borrower data when present.
    pub const fn state(&self) -> &ItemState {
        &self.state
    }
}

/// Domain invariant or transition failure.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DomainError {
    /// Item name was blank.
    EmptyName,
    /// Item name exceeded the byte limit.
    NameTooLong {
        /// Observed UTF-8 bytes.
        bytes: usize,
        /// Maximum accepted bytes.
        maximum: usize,
    },
    /// Item name contained a storage delimiter.
    InvalidNameCharacter,
    /// Borrower was blank.
    EmptyBorrower,
    /// Borrower exceeded the byte limit.
    BorrowerTooLong {
        /// Observed UTF-8 bytes.
        bytes: usize,
        /// Maximum accepted bytes.
        maximum: usize,
    },
    /// Borrower contained a storage delimiter.
    InvalidBorrowerCharacter,
    /// Allocation has no remaining ID.
    IdExhausted,
    /// No item has the requested ID.
    NotFound(ItemId),
    /// Operation was not legal from current state.
    IllegalTransition {
        /// Affected item.
        id: ItemId,
        /// Requested operation.
        operation: &'static str,
        /// Stable state label.
        from: &'static str,
    },
    /// Restored snapshot contains duplicate IDs.
    DuplicateId(ItemId),
    /// Restored next-ID metadata is inconsistent.
    InvalidNextId,
}

impl fmt::Display for DomainError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyName => write!(formatter, "item name cannot be empty"),
            Self::NameTooLong { bytes, maximum } => {
                write!(formatter, "item name is {bytes} bytes; maximum is {maximum}")
            }
            Self::InvalidNameCharacter => {
                write!(formatter, "item name cannot contain tab or line breaks")
            }
            Self::EmptyBorrower => write!(formatter, "borrower cannot be empty"),
            Self::BorrowerTooLong { bytes, maximum } => {
                write!(formatter, "borrower is {bytes} bytes; maximum is {maximum}")
            }
            Self::InvalidBorrowerCharacter => {
                write!(formatter, "borrower cannot contain tab or line breaks")
            }
            Self::IdExhausted => write!(formatter, "item ID space is exhausted"),
            Self::NotFound(id) => write!(formatter, "item {id} was not found"),
            Self::IllegalTransition {
                id,
                operation,
                from,
            } => write!(formatter, "cannot {operation} item {id} from state {from}"),
            Self::DuplicateId(id) => write!(formatter, "duplicate item ID {id}"),
            Self::InvalidNextId => {
                write!(formatter, "restored next ID is inconsistent with item IDs")
            }
        }
    }
}

impl Error for DomainError {}

/// Deterministic inventory counts.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct Counts {
    /// Available items.
    pub available: usize,
    /// Checked-out items.
    pub checked_out: usize,
    /// Retired items.
    pub retired: usize,
}

impl Counts {
    /// Returns total number of items.
    pub const fn total(self) -> usize {
        self.available + self.checked_out + self.retired
    }
}

/// Aggregate owning all items and monotonic allocation state.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Ledger {
    items: Vec<Item>,
    next_id: Option<u64>,
}

impl Default for Ledger {
    fn default() -> Self {
        Self::new()
    }
}

impl Ledger {
    /// Creates an empty ledger whose first ID is one.
    pub const fn new() -> Self {
        Self { items: Vec::new(), next_id: Some(1) }
    }

    pub(crate) fn restore(items: Vec<Item>, next_id: Option<u64>) -> Result<Self, DomainError> {
        let mut seen = HashSet::new();
        let mut maximum = 0_u64;
        for item in &items {
            if !seen.insert(item.id) {
                return Err(DomainError::DuplicateId(item.id));
            }
            maximum = maximum.max(item.id.get());
        }
        match next_id {
            Some(value) if value != 0 && value > maximum => {}
            None if maximum == u64::MAX => {}
            _ => return Err(DomainError::InvalidNextId),
        }
        Ok(Self { items, next_id })
    }

    pub(crate) const fn next_id_token(&self) -> Option<u64> {
        self.next_id
    }

    /// Borrows all items in insertion/restoration order.
    pub fn items(&self) -> &[Item] {
        &self.items
    }

    /// Adds an available item and returns its new ID.
    pub fn add(&mut self, name: String) -> Result<ItemId, DomainError> {
        validate_name(&name)?;
        let raw = self.next_id.ok_or(DomainError::IdExhausted)?;
        let id = ItemId(raw);
        self.next_id = raw.checked_add(1);
        self.items.push(Item { id, name, state: ItemState::Available });
        Ok(id)
    }

    /// Borrows an item by ID.
    pub fn find(&self, id: ItemId) -> Option<&Item> {
        self.items.iter().find(|item| item.id == id)
    }

    fn find_mut(&mut self, id: ItemId) -> Result<&mut Item, DomainError> {
        self.items.iter_mut().find(|item| item.id == id).ok_or(DomainError::NotFound(id))
    }

    /// Checks out an available item to a validated borrower.
    pub fn checkout(&mut self, id: ItemId, borrower: String) -> Result<(), DomainError> {
        validate_borrower(&borrower)?;
        let item = self.find_mut(id)?;
        if item.state != ItemState::Available {
            return Err(DomainError::IllegalTransition {
                id,
                operation: "check out",
                from: item.state.tag(),
            });
        }
        item.state = ItemState::CheckedOut { borrower };
        Ok(())
    }

    /// Returns a checked-out item to available state.
    pub fn return_item(&mut self, id: ItemId) -> Result<(), DomainError> {
        let item = self.find_mut(id)?;
        if !matches!(item.state, ItemState::CheckedOut { .. }) {
            return Err(DomainError::IllegalTransition {
                id,
                operation: "return",
                from: item.state.tag(),
            });
        }
        item.state = ItemState::Available;
        Ok(())
    }

    /// Retires an available item permanently.
    pub fn retire(&mut self, id: ItemId) -> Result<(), DomainError> {
        let item = self.find_mut(id)?;
        if item.state != ItemState::Available {
            return Err(DomainError::IllegalTransition {
                id,
                operation: "retire",
                from: item.state.tag(),
            });
        }
        item.state = ItemState::Retired;
        Ok(())
    }

    /// Searches item names with ASCII case folding.
    pub fn search(&self, query: &str) -> impl Iterator<Item = &Item> {
        let normalized = query.to_ascii_lowercase();
        self.items.iter().filter(move |item| item.name.to_ascii_lowercase().contains(&normalized))
    }

    /// Counts all states.
    pub fn counts(&self) -> Counts {
        let mut counts = Counts::default();
        for item in &self.items {
            match item.state {
                ItemState::Available => counts.available += 1,
                ItemState::CheckedOut { .. } => counts.checked_out += 1,
                ItemState::Retired => counts.retired += 1,
            }
        }
        counts
    }
}

fn validate_name(name: &str) -> Result<(), DomainError> {
    if name.trim().is_empty() {
        return Err(DomainError::EmptyName);
    }
    if name.len() > MAX_NAME_BYTES {
        return Err(DomainError::NameTooLong { bytes: name.len(), maximum: MAX_NAME_BYTES });
    }
    if has_delimiter(name) {
        return Err(DomainError::InvalidNameCharacter);
    }
    Ok(())
}

fn validate_borrower(borrower: &str) -> Result<(), DomainError> {
    if borrower.trim().is_empty() {
        return Err(DomainError::EmptyBorrower);
    }
    if borrower.len() > MAX_BORROWER_BYTES {
        return Err(DomainError::BorrowerTooLong {
            bytes: borrower.len(),
            maximum: MAX_BORROWER_BYTES,
        });
    }
    if has_delimiter(borrower) {
        return Err(DomainError::InvalidBorrowerCharacter);
    }
    Ok(())
}

fn has_delimiter(value: &str) -> bool {
    value.chars().any(|character| matches!(character, '\t' | '\n' | '\r'))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn state_carries_borrower_only_when_checked_out() {
        let mut ledger = Ledger::new();
        let id = ledger.add(String::from("meter")).expect("valid");
        ledger.checkout(id, String::from("Ada")).expect("available");
        assert_eq!(
            ledger.find(id).map(Item::state),
            Some(&ItemState::CheckedOut {
                borrower: String::from("Ada"),
            })
        );
        ledger.return_item(id).expect("checked out");
        assert_eq!(ledger.find(id).map(Item::state), Some(&ItemState::Available));
    }

    #[test]
    fn transition_failures_preserve_state() {
        let mut ledger = Ledger::new();
        let id = ledger.add(String::from("meter")).expect("valid");
        let before = ledger.clone();
        assert!(ledger.return_item(id).is_err());
        assert_eq!(ledger, before);
    }

    #[test]
    fn retired_is_terminal() {
        let mut ledger = Ledger::new();
        let id = ledger.add(String::from("meter")).expect("valid");
        ledger.retire(id).expect("available");
        assert!(ledger.checkout(id, String::from("Ada")).is_err());
        assert!(ledger.return_item(id).is_err());
        assert!(ledger.retire(id).is_err());
    }

    #[test]
    fn allocation_exhaustion_is_explicit() {
        let mut ledger = Ledger { items: Vec::new(), next_id: Some(u64::MAX) };
        let id = ledger.add(String::from("last")).expect("maximum is valid");
        assert_eq!(id.get(), u64::MAX);
        assert_eq!(ledger.add(String::from("none")), Err(DomainError::IdExhausted));
    }
}
