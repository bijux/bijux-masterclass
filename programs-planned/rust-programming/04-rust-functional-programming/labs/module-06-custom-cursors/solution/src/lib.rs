#![forbid(unsafe_code)]

use std::collections::HashSet;

pub struct Fields<'a> {
    rest: Option<&'a str>,
}

impl<'a> Fields<'a> {
    pub fn new(input: &'a str) -> Self {
        Self { rest: Some(input) }
    }
}

impl<'a> Iterator for Fields<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        loop {
            let input = self.rest.take()?;
            let (field, rest) = match input.split_once(',') {
                Some((field, rest)) => (field, Some(rest)),
                None => (input, None),
            };
            self.rest = rest;
            let field = field.trim();
            if !field.is_empty() {
                return Some(field);
            }
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        match self.rest {
            None => (0, Some(0)),
            Some(rest) => {
                let fields = rest.bytes().filter(|byte| *byte == b',').count() + 1;
                (0, Some(fields))
            }
        }
    }
}

impl std::iter::FusedIterator for Fields<'_> {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    pub id: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct EventLog {
    events: Vec<Event>,
}

impl EventLog {
    pub fn new(events: Vec<Event>) -> Self {
        Self { events }
    }

    pub fn len(&self) -> usize {
        self.events.len()
    }

    pub fn is_empty(&self) -> bool {
        self.events.is_empty()
    }
}

impl IntoIterator for EventLog {
    type Item = Event;
    type IntoIter = std::vec::IntoIter<Event>;

    fn into_iter(self) -> Self::IntoIter {
        self.events.into_iter()
    }
}

impl<'a> IntoIterator for &'a EventLog {
    type Item = &'a Event;
    type IntoIter = std::slice::Iter<'a, Event>;

    fn into_iter(self) -> Self::IntoIter {
        self.events.iter()
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Diagnostics(Vec<String>);

impl FromIterator<String> for Diagnostics {
    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = String>,
    {
        Self(iter.into_iter().collect())
    }
}

impl Extend<String> for Diagnostics {
    fn extend<I>(&mut self, iter: I)
    where
        I: IntoIterator<Item = String>,
    {
        self.0.extend(iter);
    }
}

impl Diagnostics {
    pub fn as_slice(&self) -> &[String] {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UniqueIds(Vec<u64>);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DuplicateId(pub u64);

impl UniqueIds {
    pub fn try_from_iter<I>(iter: I) -> Result<Self, DuplicateId>
    where
        I: IntoIterator<Item = u64>,
    {
        let mut seen = HashSet::new();
        let mut output = Vec::new();
        for id in iter {
            if !seen.insert(id) {
                return Err(DuplicateId(id));
            }
            output.push(id);
        }
        Ok(Self(output))
    }

    pub fn as_slice(&self) -> &[u64] {
        &self.0
    }
}

pub struct Stride<I> {
    inner: I,
    step: usize,
    first: bool,
}

impl<I> Stride<I> {
    pub fn new(inner: I, step: usize) -> Option<Self> {
        (step > 0).then_some(Self {
            inner,
            step,
            first: true,
        })
    }

    fn projected_len(&self, length: usize) -> usize {
        if self.first {
            length.div_ceil(self.step)
        } else {
            length / self.step
        }
    }
}

impl<I> Iterator for Stride<I>
where
    I: Iterator,
{
    type Item = I::Item;

    fn next(&mut self) -> Option<Self::Item> {
        if self.first {
            self.first = false;
            self.inner.next()
        } else {
            self.inner.nth(self.step - 1)
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let (lower, upper) = self.inner.size_hint();
        (
            self.projected_len(lower),
            upper.map(|value| self.projected_len(value)),
        )
    }
}

#[cfg(test)]
mod tests {
    use super::{Diagnostics, DuplicateId, Event, EventLog, Fields, Stride, UniqueIds};

    #[test]
    fn fields_skip_empty_values_and_are_fused() {
        let mut fields = Fields::new(" a,, b ,");
        assert_eq!(fields.by_ref().collect::<Vec<_>>(), vec!["a", "b"]);
        assert_eq!(fields.next(), None);
        assert_eq!(fields.next(), None);
    }

    #[test]
    fn event_log_has_borrowed_and_owned_modes() {
        let log = EventLog::new(vec![Event { id: 1 }, Event { id: 2 }]);
        assert_eq!(
            (&log).into_iter().map(|event| event.id).collect::<Vec<_>>(),
            vec![1, 2]
        );
        assert_eq!(
            log.into_iter().map(|event| event.id).collect::<Vec<_>>(),
            vec![1, 2]
        );
    }

    #[test]
    fn diagnostics_support_collection_and_incremental_extension() {
        let mut diagnostics: Diagnostics = ["a".to_owned(), "b".to_owned()]
            .into_iter()
            .collect();
        diagnostics.extend(["c".to_owned()]);
        assert_eq!(diagnostics.as_slice().len(), 3);
    }

    #[test]
    fn unique_collection_rejects_first_duplicate() {
        assert_eq!(
            UniqueIds::try_from_iter([1, 2, 1]),
            Err(DuplicateId(1))
        );
    }

    #[test]
    fn stride_and_hint_follow_next_semantics() {
        let mut stride = Stride::new(0..10, 3).unwrap();
        assert_eq!(stride.size_hint(), (4, Some(4)));
        assert_eq!(stride.next(), Some(0));
        assert_eq!(stride.size_hint(), (3, Some(3)));
        assert_eq!(stride.collect::<Vec<_>>(), vec![3, 6, 9]);
    }
}
