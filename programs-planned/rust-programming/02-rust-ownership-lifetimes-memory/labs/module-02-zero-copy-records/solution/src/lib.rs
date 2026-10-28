//! Zero-copy parsing of line-oriented key/value records.
use std::collections::HashSet;
use std::fmt;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Record<'a> {
    key: &'a str,
    value: &'a str,
    line: usize,
}
impl<'a> Record<'a> {
    pub fn key(&self) -> &'a str {
        self.key
    }
    pub fn value(&self) -> &'a str {
        self.value
    }
    pub fn line(&self) -> usize {
        self.line
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseKind {
    MissingSeparator,
    EmptyKey,
    DuplicateKey(String),
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseError {
    pub line: usize,
    pub kind: ParseKind,
}
impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.kind {
            ParseKind::MissingSeparator => write!(f, "line {} has no '=' separator", self.line),
            ParseKind::EmptyKey => write!(f, "line {} has an empty key", self.line),
            ParseKind::DuplicateKey(key) => write!(f, "line {} repeats key {key:?}", self.line),
        }
    }
}
impl std::error::Error for ParseError {
}
#[derive(Debug, PartialEq, Eq)]
pub struct RecordBook<'a> {
    source: &'a str,
    records: Vec<Record<'a>>,
}
impl<'a> RecordBook<'a> {
    pub fn parse(source: &'a str) -> Result<Self, ParseError> {
        let mut records = Vec::new();
        let mut keys = HashSet::new();
        for (zero_line, raw) in source.lines().enumerate() {
            let line = zero_line + 1;
            if raw.trim().is_empty() {
                continue;
            }
            let (key, value) = raw.split_once('=').ok_or(ParseError {
                line, kind: ParseKind::MissingSeparator
            })?;
            let key = key.trim();
            let value = value.trim();
            if key.is_empty() {
                return Err(ParseError {
                    line, kind: ParseKind::EmptyKey
                });
            }
            if !keys.insert(key) {
                return Err(ParseError {
                    line, kind: ParseKind::DuplicateKey(key.to_owned())
                });
            }
            records.push(Record {
                key, value, line
            });
        }
        Ok(Self {
            source, records
        })
    }
    pub fn source(&self) -> &'a str {
        self.source
    }
    pub fn records(&self) -> &[Record<'a>] {
        &self.records
    }
    pub fn find(&self, key: &str) -> Option<&Record<'a>> {
        self.records.iter().find(|record| record.key == key)
    }
    pub fn longest_value(&self) -> Option<&'a str> {
        self.records.iter().max_by_key(|record| record.value.len()).map(|record| record.value)
    }
}
pub fn choose_value<'left, 'right>(
left: &Record<'left>,
right: &Record<'right>,
take_left: bool,
) -> Choice<'left, 'right> {
    if take_left {
        Choice::Left(left.value)
    }
    else {
        Choice::Right(right.value)
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Choice<'left, 'right> {
    Left(&'left str),
    Right(&'right str),
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn parses_without_copying_record_text() {
        let source = String::from("name = Rust\nmode = precise\n");
        let book = RecordBook::parse(&source);
        assert!(book.is_ok());
        let book = match book {
            Ok(value) => value, Err(error) => panic!("unexpected error: {error}")
        };
        assert_eq!(book.find("name").map(Record::value), Some("Rust"));
        let source_start = source.as_ptr() as usize;
        let value = book.find("mode").map(Record::value).unwrap_or("");
        let value_start = value.as_ptr() as usize;
        assert!(value_start >= source_start && value_start < source_start + source.len());
    }
    #[test]
    fn rejects_duplicate_keys_with_context() {
        let error = RecordBook::parse("a=1\na=2");
        assert!(matches!(error, Err(ParseError {
            line: 2, kind: ParseKind::DuplicateKey(ref key)
        }) if key == "a"));
    }
    #[test]
    fn independent_sources_need_not_share_one_lifetime() {
        let long = String::from("a=longer");
        let long_book = match RecordBook::parse(&long) {
            Ok(value) => value, Err(error) => panic!("{error}")
        };
        {
            let short = String::from("b=short");
            let short_book = match RecordBook::parse(&short) {
                Ok(value) => value, Err(error) => panic!("{error}")
            };
            let left = match long_book.find("a") {
                Some(v) => v, None => panic!("missing")
            };
            let right = match short_book.find("b") {
                Some(v) => v, None => panic!("missing")
            };
            assert_eq!(choose_value(left, right, false), Choice::Right("short"));
        }
        assert_eq!(long_book.longest_value(), Some("longer"));
    }
}
