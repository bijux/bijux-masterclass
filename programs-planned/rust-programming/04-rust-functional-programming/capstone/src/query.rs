use crate::analysis::Analysis;
use crate::diagnostic::{Diagnostic, Severity};
use crate::domain::{AccountId, Event, EventKind};
use crate::ledger::AccountState;

pub fn events_for_account<'a>(
    analysis: &'a Analysis,
    account: &'a AccountId,
) -> impl Iterator<Item = &'a Event> + 'a {
    analysis
        .accepted()
        .iter()
        .filter(move |event| event.account() == account)
}

pub fn diagnostics_with_severity(
    analysis: &Analysis,
    severity: Severity,
) -> impl Iterator<Item = &Diagnostic> {
    analysis
        .diagnostics()
        .iter()
        .filter(move |item| item.severity() == severity)
}

pub fn accounts_with_minimum_balance(
    analysis: &Analysis,
    minimum: i64,
) -> impl Iterator<Item = (&AccountId, &AccountState)> {
    analysis
        .ledger()
        .accounts()
        .iter()
        .filter(move |(_, state)| state.balance() >= minimum)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TimelinePoint<'a> {
    event: &'a Event,
    balance_after: i64,
}

impl<'a> TimelinePoint<'a> {
    pub fn event(&self) -> &'a Event {
        self.event
    }

    pub fn balance_after(&self) -> i64 {
        self.balance_after
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TimelineOverflow;

pub fn account_timeline<'a>(
    analysis: &'a Analysis,
    account: &'a AccountId,
) -> impl Iterator<Item = Result<TimelinePoint<'a>, TimelineOverflow>> + 'a {
    events_for_account(analysis, account).scan(Some(0_i64), |balance, event| {
        let current = (*balance)?;
        let next = match event.kind() {
            EventKind::Deposit => current.checked_add(event.amount()),
            EventKind::Withdraw => current.checked_sub(event.amount()),
            EventKind::Open | EventKind::Close => Some(current),
        };
        match next {
            Some(value) => {
                *balance = Some(value);
                Some(Ok(TimelinePoint {
                    event,
                    balance_after: value,
                }))
            }
            None => {
                *balance = None;
                Some(Err(TimelineOverflow))
            }
        }
    })
}

#[cfg(test)]
mod tests {
    use super::{account_timeline, events_for_account};
    use crate::analysis::analyze;
    use crate::domain::AccountId;

    fn sample() -> crate::Analysis {
        analyze(concat!(
            "LEDGERFLOW-V1\n",
            "1\ta\topen\t0\tstart\n",
            "2\ta\tdeposit\t8\tfund\n",
            "3\tb\topen\t0\tother\n",
            "4\ta\twithdraw\t3\tuse\n",
        ))
    }

    #[test]
    fn query_borrows_and_preserves_source_order() {
        let analysis = sample();
        let account = AccountId::parse("a").unwrap();
        let ids: Vec<_> = events_for_account(&analysis, &account)
            .map(|event| event.id().get())
            .collect();
        assert_eq!(ids, vec![1, 2, 4]);
        assert_eq!(analysis.accepted().len(), 4);
    }

    #[test]
    fn timeline_is_a_lazy_stateful_view() {
        let analysis = sample();
        let account = AccountId::parse("a").unwrap();
        let balances: Vec<_> = account_timeline(&analysis, &account)
            .map(|point| point.unwrap().balance_after())
            .collect();
        assert_eq!(balances, vec![0, 8, 5]);
    }
}
