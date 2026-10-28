use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum DomainError {
    EmptyIdentifier(&'static str),
    IdentifierTooLong(&'static str),
    InvalidIdentifier(&'static str),
    NonFiniteValue,
    CountOverflow,
    NonMonotonicTimestamp { previous: u64, next: u64 },
    NonFiniteSum,
}

impl fmt::Display for DomainError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyIdentifier(kind) => write!(formatter, "{kind} identifier is empty"),
            Self::IdentifierTooLong(kind) => {
                write!(formatter, "{kind} identifier exceeds the configured limit")
            }
            Self::InvalidIdentifier(kind) => {
                write!(formatter, "{kind} identifier contains unsupported characters")
            }
            Self::NonFiniteValue => formatter.write_str("record value must be finite"),
            Self::CountOverflow => formatter.write_str("series count overflow"),
            Self::NonMonotonicTimestamp { previous, next } => write!(
                formatter,
                "timestamp {next} precedes the current series timestamp {previous}"
            ),
            Self::NonFiniteSum => formatter.write_str("series sum is not finite"),
        }
    }
}

impl std::error::Error for DomainError {}

fn validate_identifier(
    kind: &'static str,
    value: &str,
    max_bytes: usize,
) -> Result<(), DomainError> {
    if value.is_empty() {
        return Err(DomainError::EmptyIdentifier(kind));
    }
    if value.len() > max_bytes {
        return Err(DomainError::IdentifierTooLong(kind));
    }
    if !value
        .bytes()
        .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
    {
        return Err(DomainError::InvalidIdentifier(kind));
    }
    Ok(())
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Tenant(String);

impl Tenant {
    pub fn parse(value: &str, max_bytes: usize) -> Result<Self, DomainError> {
        validate_identifier("tenant", value, max_bytes)?;
        Ok(Self(value.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Debug for Tenant {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str("Tenant([REDACTED])")
    }
}

#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct MetricName(String);

impl MetricName {
    pub fn parse(value: &str, max_bytes: usize) -> Result<Self, DomainError> {
        validate_identifier("metric", value, max_bytes)?;
        Ok(Self(value.to_owned()))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

impl fmt::Debug for MetricName {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str("MetricName([REDACTED])")
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Record {
    tenant: Tenant,
    metric: MetricName,
    timestamp_ms: u64,
    value: f64,
}

impl Record {
    pub fn new(
        tenant: Tenant,
        metric: MetricName,
        timestamp_ms: u64,
        value: f64,
    ) -> Result<Self, DomainError> {
        if !value.is_finite() {
            return Err(DomainError::NonFiniteValue);
        }
        Ok(Self { tenant, metric, timestamp_ms, value })
    }

    pub fn tenant(&self) -> &Tenant {
        &self.tenant
    }

    pub fn metric(&self) -> &MetricName {
        &self.metric
    }

    pub const fn timestamp_ms(&self) -> u64 {
        self.timestamp_ms
    }

    pub const fn value(&self) -> f64 {
        self.value
    }

    pub(crate) fn into_parts(self) -> (Tenant, MetricName, u64, f64) {
        (self.tenant, self.metric, self.timestamp_ms, self.value)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct SeriesKey {
    tenant: Tenant,
    metric: MetricName,
}

impl SeriesKey {
    pub(crate) fn new(tenant: Tenant, metric: MetricName) -> Self {
        Self { tenant, metric }
    }

    pub fn tenant(&self) -> &Tenant {
        &self.tenant
    }

    pub fn metric(&self) -> &MetricName {
        &self.metric
    }
}

impl From<&Record> for SeriesKey {
    fn from(record: &Record) -> Self {
        Self::new(record.tenant().clone(), record.metric().clone())
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Series {
    count: u64,
    sum: f64,
    min: f64,
    max: f64,
    latest_timestamp_ms: u64,
    latest_value: f64,
}

impl Series {
    pub(crate) fn from_observation(
        timestamp_ms: u64,
        value: f64,
    ) -> Result<Self, DomainError> {
        if !value.is_finite() {
            return Err(DomainError::NonFiniteValue);
        }
        Ok(Self {
            count: 1,
            sum: value,
            min: value,
            max: value,
            latest_timestamp_ms: timestamp_ms,
            latest_value: value,
        })
    }

    pub fn from_record(record: &Record) -> Self {
        Self {
            count: 1,
            sum: record.value(),
            min: record.value(),
            max: record.value(),
            latest_timestamp_ms: record.timestamp_ms(),
            latest_value: record.value(),
        }
    }

    pub const fn count(&self) -> u64 {
        self.count
    }

    pub const fn sum(&self) -> f64 {
        self.sum
    }

    pub const fn min(&self) -> f64 {
        self.min
    }

    pub const fn max(&self) -> f64 {
        self.max
    }

    pub const fn latest_timestamp_ms(&self) -> u64 {
        self.latest_timestamp_ms
    }

    pub const fn latest_value(&self) -> f64 {
        self.latest_value
    }

    pub fn apply(&mut self, record: &Record) -> Result<(), DomainError> {
        self.apply_observation(record.timestamp_ms(), record.value())
    }

    pub fn apply_observation(
        &mut self,
        timestamp_ms: u64,
        value: f64,
    ) -> Result<(), DomainError> {
        if !value.is_finite() {
            return Err(DomainError::NonFiniteValue);
        }
        if timestamp_ms < self.latest_timestamp_ms {
            return Err(DomainError::NonMonotonicTimestamp {
                previous: self.latest_timestamp_ms,
                next: timestamp_ms,
            });
        }
        let next_count = self.count.checked_add(1).ok_or(DomainError::CountOverflow)?;
        let next_sum = self.sum + value;
        if !next_sum.is_finite() {
            return Err(DomainError::NonFiniteSum);
        }
        self.count = next_count;
        self.sum = next_sum;
        self.min = self.min.min(value);
        self.max = self.max.max(value);
        self.latest_timestamp_ms = timestamp_ms;
        self.latest_value = value;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn record(timestamp: u64, value: f64) -> Record {
        Record::new(
            Tenant::parse("acme", 32).expect("tenant"),
            MetricName::parse("requests", 32).expect("metric"),
            timestamp,
            value,
        )
        .expect("record")
    }

    #[test]
    fn update_is_rejected_before_mutation_for_old_timestamp() {
        let mut series = Series::from_record(&record(10, 2.0));
        let before = series.clone();
        assert!(series.apply(&record(9, 3.0)).is_err());
        assert_eq!(series, before);
    }

    #[test]
    fn identifiers_are_redacted_in_debug_output() {
        let tenant = Tenant::parse("secret-tenant", 64).expect("tenant");
        assert_eq!(format!("{tenant:?}"), "Tenant([REDACTED])");
    }
}
