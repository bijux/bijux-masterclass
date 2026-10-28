use bytes::Bytes;
use std::ops::Range;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OwnedRecord {
    pub key: String,
    pub value: i64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BorrowedRecord<'a> {
    pub key: &'a str,
    pub value: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum WindowError {
    InvalidUtf8,
    WrongFieldCount { line: usize },
    InvalidValue { line: usize },
    LineTooLong { line: usize },
}

#[derive(Debug, Clone)]
pub struct RecordWindow {
    bytes: Bytes,
    ranges: Vec<Range<usize>>,
}

impl RecordWindow {
    pub fn parse(bytes: Bytes, max_line_bytes: usize) -> Result<Self, WindowError> {
        let text = std::str::from_utf8(&bytes).map_err(|_| WindowError::InvalidUtf8)?;
        let mut ranges = Vec::new();
        let mut start = 0;
        for (index, line) in text.split_terminator('\n').enumerate() {
            if line.len() > max_line_bytes {
                return Err(WindowError::LineTooLong { line: index + 1 });
            }
            let end = start + line.len();
            ranges.push(start..end);
            start = end + 1;
        }
        Ok(Self { bytes, ranges })
    }

    pub fn len(&self) -> usize {
        self.ranges.len()
    }

    pub fn is_empty(&self) -> bool {
        self.ranges.is_empty()
    }

    pub fn record(&self, index: usize) -> Result<Option<BorrowedRecord<'_>>, WindowError> {
        let Some(range) = self.ranges.get(index) else {
            return Ok(None);
        };
        let line = std::str::from_utf8(&self.bytes[range.clone()]).map_err(|_| WindowError::InvalidUtf8)?;
        let mut fields = line.split('\t');
        let key = fields.next().unwrap_or_default();
        let value_text = fields.next().ok_or(WindowError::WrongFieldCount { line: index + 1 })?;
        if fields.next().is_some() || key.is_empty() {
            return Err(WindowError::WrongFieldCount { line: index + 1 });
        }
        let value = value_text
            .parse()
            .map_err(|_| WindowError::InvalidValue { line: index + 1 })?;
        Ok(Some(BorrowedRecord { key, value }))
    }

    pub fn promote(&self, index: usize) -> Result<Option<OwnedRecord>, WindowError> {
        Ok(self.record(index)?.map(|record| OwnedRecord {
            key: record.key.to_owned(),
            value: record.value,
        }))
    }

    pub fn backing_bytes(&self) -> usize {
        self.bytes.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn borrowed_record_points_into_window() {
        let window = RecordWindow::parse(Bytes::from_static(b"requests\t3\nerrors\t1\n"), 32)
            .expect("valid window");
        assert_eq!(window.len(), 2);
        assert_eq!(
            window.record(0),
            Ok(Some(BorrowedRecord { key: "requests", value: 3 }))
        );
    }

    #[test]
    fn promotion_has_independent_ownership() {
        let owned = {
            let window = RecordWindow::parse(Bytes::from_static(b"requests\t3\n"), 32)
                .expect("valid window");
            window.promote(0).expect("valid record").expect("record")
        };
        assert_eq!(owned.key, "requests");
    }

    #[test]
    fn maximum_line_is_enforced_before_field_parsing() {
        assert_eq!(
            RecordWindow::parse(Bytes::from_static(b"long-key\t1\n"), 4),
            Err(WindowError::LineTooLong { line: 1 })
        );
    }
}
