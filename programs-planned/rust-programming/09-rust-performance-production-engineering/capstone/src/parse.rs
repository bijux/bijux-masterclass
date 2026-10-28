use crate::domain::{DomainError, MetricName, Record, Tenant};
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct BorrowedRecord<'a> {
    pub tenant: &'a str,
    pub metric: &'a str,
    pub timestamp_ms: u64,
    pub value: f64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ParseError {
    LineTooLong { actual: usize, maximum: usize },
    WrongFieldCount,
    InvalidTimestamp,
    InvalidValue,
    Domain(DomainError),
}

impl fmt::Display for ParseError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::LineTooLong { actual, maximum } => {
                write!(formatter, "line contains {actual} bytes; maximum is {maximum}")
            }
            Self::WrongFieldCount => formatter.write_str("expected exactly four tab-separated fields"),
            Self::InvalidTimestamp => formatter.write_str("timestamp must be an unsigned integer"),
            Self::InvalidValue => formatter.write_str("value must be a finite floating-point number"),
            Self::Domain(error) => write!(formatter, "{error}"),
        }
    }
}

impl std::error::Error for ParseError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Domain(error) => Some(error),
            _ => None,
        }
    }
}

impl From<DomainError> for ParseError {
    fn from(value: DomainError) -> Self {
        Self::Domain(value)
    }
}

pub fn parse_borrowed(
    line: &str,
    max_line_bytes: usize,
) -> Result<BorrowedRecord<'_>, ParseError> {
    if line.len() > max_line_bytes {
        return Err(ParseError::LineTooLong {
            actual: line.len(),
            maximum: max_line_bytes,
        });
    }
    let mut fields = line.split('\t');
    let tenant = fields.next().unwrap_or_default();
    let metric = fields.next().ok_or(ParseError::WrongFieldCount)?;
    let timestamp = fields.next().ok_or(ParseError::WrongFieldCount)?;
    let value = fields.next().ok_or(ParseError::WrongFieldCount)?;
    if fields.next().is_some() {
        return Err(ParseError::WrongFieldCount);
    }

    let timestamp_ms = timestamp.parse().map_err(|_| ParseError::InvalidTimestamp)?;
    let value = value.parse::<f64>().map_err(|_| ParseError::InvalidValue)?;
    if !value.is_finite() {
        return Err(ParseError::InvalidValue);
    }
    Ok(BorrowedRecord { tenant, metric, timestamp_ms, value })
}

pub fn promote(
    borrowed: BorrowedRecord<'_>,
    max_identifier_bytes: usize,
) -> Result<Record, ParseError> {
    let tenant = Tenant::parse(borrowed.tenant, max_identifier_bytes)?;
    let metric = MetricName::parse(borrowed.metric, max_identifier_bytes)?;
    Ok(Record::new(tenant, metric, borrowed.timestamp_ms, borrowed.value)?)
}

pub fn parse_record(
    line: &str,
    max_line_bytes: usize,
    max_identifier_bytes: usize,
) -> Result<Record, ParseError> {
    promote(parse_borrowed(line, max_line_bytes)?, max_identifier_bytes)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_and_promotes_valid_record() {
        let record = parse_record("acme\trequests\t10\t2.5", 128, 32).expect("record");
        assert_eq!(record.tenant().as_str(), "acme");
        assert_eq!(record.metric().as_str(), "requests");
    }

    #[test]
    fn extra_field_is_rejected() {
        assert_eq!(
            parse_borrowed("a\tb\t1\t2\textra", 128),
            Err(ParseError::WrongFieldCount)
        );
    }

    #[test]
    fn non_finite_value_is_rejected() {
        assert_eq!(
            parse_borrowed("a\tb\t1\tNaN", 128),
            Err(ParseError::InvalidValue)
        );
    }
}
