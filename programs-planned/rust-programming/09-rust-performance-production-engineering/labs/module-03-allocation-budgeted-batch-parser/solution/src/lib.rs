#[derive(Debug, Clone, Copy)]
pub struct Limits {
    pub max_records: usize,
    pub max_input_bytes: usize,
    pub max_key_bytes: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BorrowedRecord<'a> {
    pub key: &'a str,
    pub value: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Record {
    pub key: String,
    pub value: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    TooManyBytes,
    TooManyRecords,
    WrongFieldCount { line: usize },
    InvalidKey { line: usize },
    InvalidValue { line: usize },
}

fn valid_key(key: &str, max_bytes: usize) -> bool {
    !key.is_empty()
        && key.len() <= max_bytes
        && key.bytes().all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
}

pub fn parse_borrowed(
    line: &str,
    line_number: usize,
    limits: Limits,
) -> Result<BorrowedRecord<'_>, ParseError> {
    let mut fields = line.split('\t');
    let key = fields.next().unwrap_or_default();
    let value_text = fields.next().ok_or(ParseError::WrongFieldCount { line: line_number })?;
    if fields.next().is_some() {
        return Err(ParseError::WrongFieldCount { line: line_number });
    }
    if !valid_key(key, limits.max_key_bytes) {
        return Err(ParseError::InvalidKey { line: line_number });
    }
    let value = value_text
        .parse::<i64>()
        .map_err(|_| ParseError::InvalidValue { line: line_number })?;
    Ok(BorrowedRecord { key, value })
}

pub fn parse_batch(input: &str, limits: Limits) -> Result<Vec<Record>, ParseError> {
    if input.len() > limits.max_input_bytes {
        return Err(ParseError::TooManyBytes);
    }
    let count = input.lines().count();
    if count > limits.max_records {
        return Err(ParseError::TooManyRecords);
    }
    let mut records = Vec::with_capacity(count);
    for (index, line) in input.lines().enumerate() {
        let borrowed = parse_borrowed(line, index + 1, limits)?;
        records.push(Record { key: borrowed.key.to_owned(), value: borrowed.value });
    }
    Ok(records)
}

#[cfg(test)]
mod tests {
    use super::*;

    const LIMITS: Limits = Limits { max_records: 2, max_input_bytes: 64, max_key_bytes: 12 };

    #[test]
    fn promotes_only_after_validation() {
        assert_eq!(
            parse_batch("requests\t3\nerrors\t1", LIMITS),
            Ok(vec![
                Record { key: "requests".into(), value: 3 },
                Record { key: "errors".into(), value: 1 },
            ])
        );
    }

    #[test]
    fn batch_failure_returns_no_partial_vector() {
        assert_eq!(
            parse_batch("good\t1\nbad key\t2", LIMITS),
            Err(ParseError::InvalidKey { line: 2 })
        );
    }

    #[test]
    fn limits_are_checked() {
        assert_eq!(parse_batch("a\t1\nb\t2\nc\t3", LIMITS), Err(ParseError::TooManyRecords));
    }
}
