use crate::domain::{AccountId, EventId};
use std::rc::Rc;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AuditDisposition {
    Accepted,
    Rejected,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AuditEntry {
    line: usize,
    event_id: Option<EventId>,
    account: Option<AccountId>,
    disposition: AuditDisposition,
    code: Option<&'static str>,
}

impl AuditEntry {
    pub fn accepted(line: usize, event_id: EventId, account: AccountId) -> Self {
        Self {
            line,
            event_id: Some(event_id),
            account: Some(account),
            disposition: AuditDisposition::Accepted,
            code: None,
        }
    }

    pub fn rejected(
        line: usize,
        event_id: Option<EventId>,
        account: Option<AccountId>,
        code: &'static str,
    ) -> Self {
        Self {
            line,
            event_id,
            account,
            disposition: AuditDisposition::Rejected,
            code: Some(code),
        }
    }

    pub fn line(&self) -> usize {
        self.line
    }

    pub fn event_id(&self) -> Option<EventId> {
        self.event_id
    }

    pub fn account(&self) -> Option<&AccountId> {
        self.account.as_ref()
    }

    pub fn disposition(&self) -> AuditDisposition {
        self.disposition
    }

    pub fn code(&self) -> Option<&'static str> {
        self.code
    }
}

#[derive(Debug)]
struct AuditNode {
    entry: AuditEntry,
    previous: Option<Rc<AuditNode>>,
    len: usize,
}

#[derive(Debug, Clone, Default)]
pub struct AuditTrail {
    head: Option<Rc<AuditNode>>,
}

impl AuditTrail {
    pub fn push(&self, entry: AuditEntry) -> Self {
        let len = self.len() + 1;
        Self {
            head: Some(Rc::new(AuditNode {
                entry,
                previous: self.head.clone(),
                len,
            })),
        }
    }

    pub fn len(&self) -> usize {
        self.head.as_ref().map_or(0, |node| node.len)
    }

    pub fn is_empty(&self) -> bool {
        self.head.is_none()
    }

    pub fn newest_first(&self) -> AuditIter<'_> {
        AuditIter {
            next: self.head.as_deref(),
        }
    }

    pub fn chronological(&self) -> Vec<&AuditEntry> {
        let mut entries: Vec<_> = self.newest_first().collect();
        entries.reverse();
        entries
    }

    #[cfg(test)]
    fn shares_history_with(&self, older: &Self) -> bool {
        let mut cursor = self.head.as_deref();
        while let Some(node) = cursor {
            if older
                .head
                .as_ref()
                .is_some_and(|head| std::ptr::eq(node, Rc::as_ptr(head)))
            {
                return true;
            }
            cursor = node.previous.as_deref();
        }
        older.head.is_none()
    }
}

pub struct AuditIter<'a> {
    next: Option<&'a AuditNode>,
}

impl<'a> Iterator for AuditIter<'a> {
    type Item = &'a AuditEntry;

    fn next(&mut self) -> Option<Self::Item> {
        let node = self.next?;
        self.next = node.previous.as_deref();
        Some(&node.entry)
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let remaining = self.next.map_or(0, |node| node.len);
        (remaining, Some(remaining))
    }
}

impl ExactSizeIterator for AuditIter<'_> {}
impl std::iter::FusedIterator for AuditIter<'_> {}

#[cfg(test)]
mod tests {
    use super::{AuditDisposition, AuditEntry, AuditTrail};
    use crate::domain::{AccountId, EventId};

    fn entry(line: usize) -> AuditEntry {
        AuditEntry::accepted(
            line,
            EventId::new(line as u64).unwrap(),
            AccountId::parse("acct").unwrap(),
        )
    }

    #[test]
    fn versions_share_the_older_tail() {
        let empty = AuditTrail::default();
        let first = empty.push(entry(1));
        let second = first.push(entry(2));
        assert!(second.shares_history_with(&first));
        assert_eq!(first.len(), 1);
        assert_eq!(second.len(), 2);
        assert_eq!(first.chronological()[0].line(), 1);
    }

    #[test]
    fn iterator_is_exact_and_fused() {
        let trail = AuditTrail::default().push(entry(1)).push(entry(2));
        let mut iter = trail.newest_first();
        assert_eq!(iter.len(), 2);
        assert_eq!(iter.next().map(AuditEntry::line), Some(2));
        assert_eq!(iter.len(), 1);
        assert_eq!(iter.next().map(AuditEntry::disposition), Some(AuditDisposition::Accepted));
        assert_eq!(iter.next(), None);
        assert_eq!(iter.next(), None);
    }
}
