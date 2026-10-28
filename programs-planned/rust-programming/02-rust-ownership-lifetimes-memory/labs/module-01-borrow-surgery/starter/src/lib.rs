//! Baseline account topology for the Borrow Surgery laboratory.
//!
//! Duplicate protection, mutable lookup, label replacement, notes, and
//! transactional two-account transfer remain the learner's work.

/// One account owned by a [`Book`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Account {
    id: u64,
    label: String,
    balance: i64,
}

impl Account {
    /// Creates one starter account.
    pub fn new(id: u64, label: impl Into<String>, balance: i64) -> Self {
        Self {
            id,
            label: label.into(),
            balance,
        }
    }

    /// Returns domain identity.
    pub const fn id(&self) -> u64 {
        self.id
    }

    /// Borrows the owned label.
    pub fn label(&self) -> &str {
        &self.label
    }

    /// Returns the current balance.
    pub const fn balance(&self) -> i64 {
        self.balance
    }
}

/// Vector-owned account aggregate before disjoint mutation is added.
#[derive(Debug, Default)]
pub struct Book {
    accounts: Vec<Account>,
}

impl Book {
    /// Adds one account without yet enforcing the final duplicate-ID contract.
    pub fn add_baseline(&mut self, account: Account) {
        self.accounts.push(account);
    }

    /// Borrows all accounts in storage order.
    pub fn accounts(&self) -> &[Account] {
        &self.accounts
    }

    /// Finds one account through shared access.
    pub fn find(&self, id: u64) -> Option<&Account> {
        self.accounts.iter().find(|account| account.id == id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_lookup_borrows_without_cloning() {
        let mut book = Book::default();
        book.add_baseline(Account::new(1, "cash", 10));
        assert_eq!(book.find(1).map(Account::label), Some("cash"));
        assert_eq!(book.accounts().len(), 1);
    }
}
