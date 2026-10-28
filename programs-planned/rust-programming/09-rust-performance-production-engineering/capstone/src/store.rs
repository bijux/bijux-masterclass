use crate::domain::{DomainError, Record, Series, SeriesKey};
use std::collections::{BTreeMap, btree_map::Entry};
use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum StoreError {
    Domain(DomainError),
    SeriesLimit,
    IdentifierStorageLimit,
    SnapshotTooLarge,
}

impl fmt::Display for StoreError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Domain(error) => write!(formatter, "{error}"),
            Self::SeriesLimit => formatter.write_str("series limit reached"),
            Self::IdentifierStorageLimit => {
                formatter.write_str("identifier storage limit reached")
            }
            Self::SnapshotTooLarge => formatter.write_str("snapshot exceeds configured byte limit"),
        }
    }
}

impl std::error::Error for StoreError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Domain(error) => Some(error),
            _ => None,
        }
    }
}

impl From<DomainError> for StoreError {
    fn from(value: DomainError) -> Self {
        Self::Domain(value)
    }
}

#[derive(Debug, Clone)]
pub struct Store {
    series: BTreeMap<SeriesKey, Series>,
    max_series: usize,
    max_identifier_storage_bytes: usize,
    identifier_storage_bytes: usize,
}

#[derive(Debug, Clone, PartialEq)]
pub struct SnapshotRow {
    pub tenant: String,
    pub metric: String,
    pub series: Series,
}

#[derive(Debug, Clone, PartialEq)]
pub struct Snapshot {
    pub rows: Vec<SnapshotRow>,
}

impl Store {
    pub fn new(max_series: usize, max_identifier_storage_bytes: usize) -> Self {
        Self {
            series: BTreeMap::new(),
            max_series,
            max_identifier_storage_bytes,
            identifier_storage_bytes: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.series.len()
    }

    pub fn is_empty(&self) -> bool {
        self.series.is_empty()
    }

    pub fn identifier_storage_bytes(&self) -> usize {
        self.identifier_storage_bytes
    }

    pub fn apply(&mut self, record: Record) -> Result<(), StoreError> {
        let (tenant, metric, timestamp_ms, value) = record.into_parts();
        let key = SeriesKey::new(tenant, metric);
        let current_series = self.series.len();
        let current_identifier_bytes = self.identifier_storage_bytes;
        let additional_identifier_bytes = key
            .tenant()
            .as_str()
            .len()
            .checked_add(key.metric().as_str().len())
            .ok_or(StoreError::IdentifierStorageLimit)?;

        match self.series.entry(key) {
            Entry::Occupied(mut entry) => {
                entry.get_mut().apply_observation(timestamp_ms, value)?;
            }
            Entry::Vacant(entry) => {
                if current_series >= self.max_series {
                    return Err(StoreError::SeriesLimit);
                }
                let next_storage = current_identifier_bytes
                    .checked_add(additional_identifier_bytes)
                    .ok_or(StoreError::IdentifierStorageLimit)?;
                if next_storage > self.max_identifier_storage_bytes {
                    return Err(StoreError::IdentifierStorageLimit);
                }
                entry.insert(Series::from_observation(timestamp_ms, value)?);
                self.identifier_storage_bytes = next_storage;
            }
        }
        Ok(())
    }

    pub fn snapshot(&self) -> Snapshot {
        Snapshot {
            rows: self
                .series
                .iter()
                .map(|(key, series)| SnapshotRow {
                    tenant: key.tenant().as_str().to_owned(),
                    metric: key.metric().as_str().to_owned(),
                    series: series.clone(),
                })
                .collect(),
        }
    }
}

impl Snapshot {
    pub fn render(&self, max_bytes: usize) -> Result<String, StoreError> {
        use std::fmt::Write as _;

        let mut output = String::new();
        for row in &self.rows {
            let mut rendered_row = String::new();
            writeln!(
                rendered_row,
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",
                row.tenant,
                row.metric,
                row.series.count(),
                row.series.sum(),
                row.series.min(),
                row.series.max(),
                row.series.latest_timestamp_ms(),
                row.series.latest_value()
            )
            .map_err(|_| StoreError::SnapshotTooLarge)?;
            let next_length = output
                .len()
                .checked_add(rendered_row.len())
                .ok_or(StoreError::SnapshotTooLarge)?;
            if next_length > max_bytes {
                return Err(StoreError::SnapshotTooLarge);
            }
            output.push_str(&rendered_row);
        }
        Ok(output)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::{MetricName, Tenant};

    fn record(tenant: &str, metric: &str, timestamp: u64, value: f64) -> Record {
        Record::new(
            Tenant::parse(tenant, 64).expect("tenant"),
            MetricName::parse(metric, 64).expect("metric"),
            timestamp,
            value,
        )
        .expect("record")
    }

    #[test]
    fn snapshot_order_is_deterministic() {
        let mut store = Store::new(10, 1024);
        store.apply(record("z", "b", 1, 1.0)).expect("apply");
        store.apply(record("a", "c", 1, 2.0)).expect("apply");
        store.apply(record("a", "b", 1, 3.0)).expect("apply");
        let rows = store.snapshot().rows;
        let keys: Vec<_> = rows
            .iter()
            .map(|row| (row.tenant.as_str(), row.metric.as_str()))
            .collect();
        assert_eq!(keys, vec![("a", "b"), ("a", "c"), ("z", "b")]);
    }

    #[test]
    fn new_series_limit_is_failure_atomic() {
        let mut store = Store::new(1, 1024);
        store.apply(record("a", "x", 1, 1.0)).expect("first");
        assert_eq!(store.apply(record("b", "y", 1, 1.0)), Err(StoreError::SeriesLimit));
        assert_eq!(store.len(), 1);
    }
}
