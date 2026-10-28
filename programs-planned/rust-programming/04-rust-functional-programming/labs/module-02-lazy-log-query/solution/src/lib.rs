#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum Level {
    Debug,
    Info,
    Warn,
    Error,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LogEntry {
    pub level: Level,
    pub message: String,
}

impl LogEntry {
    pub fn new(level: Level, message: impl Into<String>) -> Self {
        Self {
            level,
            message: message.into(),
        }
    }
}

pub fn query<'a>(
    entries: &'a [LogEntry],
    minimum: Level,
    term: &'a str,
) -> impl Iterator<Item = &'a LogEntry> + 'a {
    entries
        .iter()
        .filter(move |entry| entry.level >= minimum && entry.message.contains(term))
}

pub fn consume_until<'a, I>(iterator: &mut I, marker: &str) -> Vec<&'a str>
where
    I: Iterator<Item = &'a str>,
{
    iterator
        .by_ref()
        .take_while(|line| *line != marker)
        .collect()
}

pub fn take_before_preserving<'a, I>(
    iterator: &mut std::iter::Peekable<I>,
    marker: &str,
) -> Vec<&'a str>
where
    I: Iterator<Item = &'a str>,
{
    let mut output = Vec::new();
    while iterator.peek().is_some_and(|line| *line != marker) {
        if let Some(line) = iterator.next() {
            output.push(line);
        }
    }
    output
}

#[cfg(test)]
mod tests {
    use super::{Level, LogEntry, consume_until, query, take_before_preserving};
    use std::cell::Cell;

    #[test]
    fn borrowed_query_preserves_source() {
        let entries = vec![
            LogEntry::new(Level::Info, "ok"),
            LogEntry::new(Level::Error, "disk"),
        ];
        let matches: Vec<_> = query(&entries, Level::Warn, "disk").collect();
        assert_eq!(matches.len(), 1);
        assert_eq!(entries.len(), 2);
    }

    #[test]
    fn take_limits_predicate_work() {
        let calls = Cell::new(0);
        let data = [1, 2, 3, 4];
        let matches: Vec<_> = data
            .iter()
            .filter(|value| {
                calls.set(calls.get() + 1);
                **value % 2 == 0
            })
            .take(1)
            .collect();
        assert_eq!(matches, vec![&2]);
        assert_eq!(calls.get(), 2);
    }

    #[test]
    fn take_while_consumes_the_boundary_item() {
        let mut iterator = ["a", "STOP", "b"].into_iter();
        assert_eq!(consume_until(&mut iterator, "STOP"), vec!["a"]);
        assert_eq!(iterator.collect::<Vec<_>>(), vec!["b"]);
    }

    #[test]
    fn peekable_variant_preserves_the_boundary_item() {
        let mut iterator = ["a", "STOP", "b"].into_iter().peekable();
        assert_eq!(take_before_preserving(&mut iterator, "STOP"), vec!["a"]);
        assert_eq!(iterator.next(), Some("STOP"));
    }
}
