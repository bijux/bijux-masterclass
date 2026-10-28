use crate::diagnostic::{Diagnostic, DiagnosticKind};
use crate::domain::{AccountId, Event, EventKind};
use std::collections::{BTreeMap, btree_map::Entry};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccountStatus {
    Open,
    Closed,
}

impl AccountStatus {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Open => "open",
            Self::Closed => "closed",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountState {
    balance: i64,
    status: AccountStatus,
    accepted_events: usize,
}

impl AccountState {
    fn opened() -> Self {
        Self {
            balance: 0,
            status: AccountStatus::Open,
            accepted_events: 1,
        }
    }

    pub fn balance(&self) -> i64 {
        self.balance
    }

    pub fn status(&self) -> AccountStatus {
        self.status
    }

    pub fn accepted_events(&self) -> usize {
        self.accepted_events
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Ledger {
    accounts: BTreeMap<AccountId, AccountState>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TransitionFailure {
    ledger: Ledger,
    diagnostic: Diagnostic,
}

impl TransitionFailure {
    pub fn into_parts(self) -> (Ledger, Diagnostic) {
        (self.ledger, self.diagnostic)
    }
}

enum Mutation {
    Insert,
    SetBalance(i64),
    Close,
}

impl Ledger {
    pub fn accounts(&self) -> &BTreeMap<AccountId, AccountState> {
        &self.accounts
    }

    pub fn get(&self, account: &AccountId) -> Option<&AccountState> {
        self.accounts.get(account)
    }

    pub fn apply(mut self, event: &Event) -> Result<Self, TransitionFailure> {
        let mutation = match self.plan(event) {
            Ok(value) => value,
            Err(diagnostic) => {
                return Err(TransitionFailure {
                    ledger: self,
                    diagnostic,
                });
            }
        };

        match mutation {
            Mutation::Insert => match self.accounts.entry(event.account().clone()) {
                Entry::Vacant(slot) => {
                    slot.insert(AccountState::opened());
                }
                Entry::Occupied(occupied) => {
                    drop(occupied);
                    return Err(TransitionFailure {
                        ledger: self,
                        diagnostic: Diagnostic::error(
                            event.line(),
                            DiagnosticKind::AccountAlreadyExists {
                                account: event.account().clone(),
                            },
                        ),
                    });
                }
            },
            Mutation::SetBalance(balance) => {
                let Some(account) = self.accounts.get_mut(event.account()) else {
                    return Err(TransitionFailure {
                        ledger: self,
                        diagnostic: Diagnostic::error(
                            event.line(),
                            DiagnosticKind::AccountNotFound {
                                account: event.account().clone(),
                            },
                        ),
                    });
                };
                account.balance = balance;
                account.accepted_events += 1;
            }
            Mutation::Close => {
                let Some(account) = self.accounts.get_mut(event.account()) else {
                    return Err(TransitionFailure {
                        ledger: self,
                        diagnostic: Diagnostic::error(
                            event.line(),
                            DiagnosticKind::AccountNotFound {
                                account: event.account().clone(),
                            },
                        ),
                    });
                };
                account.status = AccountStatus::Closed;
                account.accepted_events += 1;
            }
        }
        Ok(self)
    }

    fn plan(&self, event: &Event) -> Result<Mutation, Diagnostic> {
        match event.kind() {
            EventKind::Open => self.plan_open(event),
            EventKind::Deposit => self.plan_deposit(event),
            EventKind::Withdraw => self.plan_withdraw(event),
            EventKind::Close => self.plan_close(event),
        }
    }

    fn plan_open(&self, event: &Event) -> Result<Mutation, Diagnostic> {
        if event.amount() != 0 {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::LifecycleAmountMustBeZero {
                    kind: event.kind(),
                    amount: event.amount(),
                },
            ));
        }
        if self.accounts.contains_key(event.account()) {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::AccountAlreadyExists {
                    account: event.account().clone(),
                },
            ));
        }
        Ok(Mutation::Insert)
    }

    fn open_account(&self, event: &Event) -> Result<&AccountState, Diagnostic> {
        let Some(account) = self.accounts.get(event.account()) else {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::AccountNotFound {
                    account: event.account().clone(),
                },
            ));
        };
        if account.status == AccountStatus::Closed {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::AccountClosed {
                    account: event.account().clone(),
                },
            ));
        }
        Ok(account)
    }

    fn require_positive_amount(&self, event: &Event) -> Result<(), Diagnostic> {
        if event.amount() <= 0 {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::TransferAmountMustBePositive {
                    kind: event.kind(),
                    amount: event.amount(),
                },
            ));
        }
        Ok(())
    }

    fn plan_deposit(&self, event: &Event) -> Result<Mutation, Diagnostic> {
        self.require_positive_amount(event)?;
        let account = self.open_account(event)?;
        let Some(balance) = account.balance.checked_add(event.amount()) else {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::BalanceOverflow {
                    account: event.account().clone(),
                },
            ));
        };
        Ok(Mutation::SetBalance(balance))
    }

    fn plan_withdraw(&self, event: &Event) -> Result<Mutation, Diagnostic> {
        self.require_positive_amount(event)?;
        let account = self.open_account(event)?;
        if event.amount() > account.balance {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::InsufficientFunds {
                    account: event.account().clone(),
                    available: account.balance,
                    requested: event.amount(),
                },
            ));
        }
        Ok(Mutation::SetBalance(account.balance - event.amount()))
    }

    fn plan_close(&self, event: &Event) -> Result<Mutation, Diagnostic> {
        if event.amount() != 0 {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::LifecycleAmountMustBeZero {
                    kind: event.kind(),
                    amount: event.amount(),
                },
            ));
        }
        let account = self.open_account(event)?;
        if account.balance != 0 {
            return Err(Diagnostic::error(
                event.line(),
                DiagnosticKind::BalanceMustBeZeroToClose {
                    account: event.account().clone(),
                    balance: account.balance,
                },
            ));
        }
        Ok(Mutation::Close)
    }
}

#[cfg(test)]
mod tests {
    use super::{AccountStatus, Ledger};
    use crate::domain::{AccountId, Event, EventId, EventKind};

    fn event(line: usize, id: u64, kind: EventKind, amount: i64) -> Event {
        Event::new(
            line,
            EventId::new(id).unwrap(),
            AccountId::parse("acct").unwrap(),
            kind,
            amount,
            None,
        )
    }

    #[test]
    fn rejected_transition_returns_the_unchanged_ledger() {
        let ledger = Ledger::default().apply(&event(1, 1, EventKind::Open, 0)).unwrap();
        let failure = ledger
            .clone()
            .apply(&event(2, 2, EventKind::Withdraw, 1))
            .unwrap_err();
        let (recovered, _) = failure.into_parts();
        assert_eq!(recovered, ledger);
    }

    #[test]
    fn accepted_sequence_closes_zero_balance_account() {
        let ledger = Ledger::default()
            .apply(&event(1, 1, EventKind::Open, 0))
            .unwrap()
            .apply(&event(2, 2, EventKind::Deposit, 5))
            .unwrap()
            .apply(&event(3, 3, EventKind::Withdraw, 5))
            .unwrap()
            .apply(&event(4, 4, EventKind::Close, 0))
            .unwrap();
        let account = ledger.get(&AccountId::parse("acct").unwrap()).unwrap();
        assert_eq!(account.balance(), 0);
        assert_eq!(account.status(), AccountStatus::Closed);
        assert_eq!(account.accepted_events(), 4);
    }
}
