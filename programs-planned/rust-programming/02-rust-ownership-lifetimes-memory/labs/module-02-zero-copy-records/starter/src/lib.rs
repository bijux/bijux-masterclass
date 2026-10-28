//! Borrowed-record vocabulary for the zero-copy parsing laboratory.
//!
//! Aggregate parsing, duplicate detection, line context, and independent source
//! lifetime selection remain the learner's work.

/// One key/value pair borrowed from an input source.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Record<'source> {
    /// Borrowed key slice.
    pub key: &'source str,
    /// Borrowed value slice.
    pub value: &'source str,
}

/// Splits one record and returns slices of the supplied line.
pub fn split_record(line: &str) -> Option<Record<'_>> {
    let (key, value) = line.split_once('=')?;
    Some(Record {
        key: key.trim(),
        value: value.trim(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn returns_slices_of_input() {
        let source = String::from("name = rust");
        let record = split_record(&source).expect("one separator exists");
        assert_eq!(
            record,
            Record {
                key: "name",
                value: "rust",
            }
        );
        let range = source.as_ptr_range();
        assert!(range.contains(&record.key.as_ptr()));
        assert!(range.contains(&record.value.as_ptr()));
    }
}
