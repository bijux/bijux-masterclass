//! Borrow-aware account operations with transactional balance updates.
use std::fmt;
use std::mem;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Account {
    id: u64,
    label: String,
    balance: i64,
    notes: Vec<String>,
}
impl Account {
    pub fn new(id: u64, label: impl Into<String>, balance: i64) -> Self {
        Self {
            id, label: label.into(), balance, notes: Vec::new()
        }
    }
    pub fn id(&self) -> u64 {
        self.id
    }
    pub fn label(&self) -> &str {
        &self.label
    }
    pub fn balance(&self) -> i64 {
        self.balance
    }
    pub fn notes(&self) -> &[String] {
        &self.notes
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BookError {
    DuplicateId(u64),
    Missing(u64),
    SameAccount(u64),
    NonPositiveAmount(i64),
    InsufficientFunds {
        id: u64, available: i64, requested: i64
    },
    ArithmeticOverflow,
}
impl fmt::Display for BookError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DuplicateId(id) => write!(f, "duplicate account id {id}"),
            Self::Missing(id) => write!(f, "account {id} does not exist"),
            Self::SameAccount(id) => write!(f, "source and destination are both account {id}"),
            Self::NonPositiveAmount(amount) => write!(f, "transfer amount must be positive, got {amount}"),
            Self::InsufficientFunds {
                id, available, requested
            }
            => write!(f, "account {id} has {available}, requested {requested}"),
            Self::ArithmeticOverflow => write!(f, "balance arithmetic overflowed"),
        }
    }
}
impl std::error::Error for BookError {
}
#[derive(Debug, Default, PartialEq, Eq)]
pub struct Book {
    accounts: Vec<Account>,
}
impl Book {
    pub fn insert(&mut self, account: Account) -> Result<(), BookError> {
        if self.accounts.iter().any(|current| current.id == account.id) {
            return Err(BookError::DuplicateId(account.id));
        }
        self.accounts.push(account);
        Ok(())
    }
    pub fn accounts(&self) -> &[Account] {
        &self.accounts
    }
    pub fn find(&self, id: u64) -> Option<&Account> {
        self.accounts.iter().find(|account| account.id == id)
    }
    pub fn find_mut(&mut self, id: u64) -> Option<&mut Account> {
        self.accounts.iter_mut().find(|account| account.id == id)
    }
    pub fn rename(&mut self, id: u64, next: String) -> Result<String, BookError> {
        let account = self.find_mut(id).ok_or(BookError::Missing(id))?;
        Ok(mem::replace(&mut account.label, next))
    }
    pub fn add_note(&mut self, id: u64, note: String) -> Result<(), BookError> {
        let account = self.find_mut(id).ok_or(BookError::Missing(id))?;
        account.notes.push(note);
        Ok(())
    }
    pub fn transfer(&mut self, source: u64, target: u64, amount: i64) -> Result<(), BookError> {
        if amount <= 0 {
            return Err(BookError::NonPositiveAmount(amount));
        }
        if source == target {
            return Err(BookError::SameAccount(source));
        }
        let source_index = self.accounts.iter().position(|a| a.id == source).ok_or(BookError::Missing(source))?;
        let target_index = self.accounts.iter().position(|a| a.id == target).ok_or(BookError::Missing(target))?;
        let (from, to) = two_mut(
            &mut self.accounts,
            source_index,
            target_index,
        )
        .expect("indices were proven distinct and in bounds");
        if from.balance < amount {
            return Err(BookError::InsufficientFunds {
                id: source, available: from.balance, requested: amount
            });
        }
        let next_from = from.balance.checked_sub(amount).ok_or(BookError::ArithmeticOverflow)?;
        let next_to = to.balance.checked_add(amount).ok_or(BookError::ArithmeticOverflow)?;
        from.balance = next_from;
        to.balance = next_to;
        Ok(())
    }
}
fn two_mut<T>(slice: &mut [T], left: usize, right: usize) -> Option<(&mut T, &mut T)> {
    if left == right || left >= slice.len() || right >= slice.len() {
        return None;
    }
    if left < right {
        let (before, after) = slice.split_at_mut(right);
        Some((&mut before[left], &mut after[0]))
    }
    else {
        let (before, after) = slice.split_at_mut(left);
        Some((&mut after[0], &mut before[right]))
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    fn book() -> Book {
        let mut book = Book::default();
        assert!(book.insert(Account::new(1, "cash", 100)).is_ok());
        assert!(book.insert(Account::new(2, "reserve", 20)).is_ok());
        book
    }
    #[test]
    fn transfer_mutates_two_disjoint_accounts() {
        let mut book = book();
        assert_eq!(book.transfer(1, 2, 30), Ok(()));
        assert_eq!(book.find(1).map(Account::balance), Some(70));
        assert_eq!(book.find(2).map(Account::balance), Some(50));
    }
    #[test]
    fn failed_transfer_is_transactional() {
        let mut book = book();
        let before = book.accounts.clone();
        assert!(matches!(book.transfer(1, 2, 200), Err(BookError::InsufficientFunds {
            ..
        })));
        assert_eq!(book.accounts, before);
    }
    #[test]
    fn target_overflow_changes_nothing() {
        let mut book = Book::default();
        assert!(book.insert(Account::new(1, "source", 10)).is_ok());
        assert!(book.insert(Account::new(2, "target", i64::MAX)).is_ok());
        let before = book.accounts.clone();
        assert_eq!(book.transfer(1, 2, 1), Err(BookError::ArithmeticOverflow));
        assert_eq!(book.accounts, before);
    }
    #[test]
    fn rename_returns_owned_previous_label() {
        let mut book = book();
        assert_eq!(book.rename(1, String::from("operating")), Ok(String::from("cash")));
        assert_eq!(book.find(1).map(Account::label), Some("operating"));
    }
}
