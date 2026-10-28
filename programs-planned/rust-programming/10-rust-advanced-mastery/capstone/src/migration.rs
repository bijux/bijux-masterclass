use std::{collections::BTreeMap, fs, path::Path};

use crate::{Record, Snapshot, Store, StoreError};

pub fn migrate_v0<const MAX_RECORD: usize, const TX_CAP: usize>(
    source: &Path,
    destination: &Store<MAX_RECORD, TX_CAP>,
) -> Result<Snapshot<MAX_RECORD>, StoreError> {
    let text = fs::read_to_string(source)
        .map_err(|error| StoreError::io("read legacy source", source, error))?;
    let mut records = BTreeMap::new();

    for (index, raw) in text.lines().enumerate() {
        let line = index + 1;
        if raw.is_empty() || raw.starts_with('#') {
            continue;
        }
        let (key, value) = raw
            .split_once('=')
            .ok_or_else(|| StoreError::Migration {
                line,
                message: "expected key=value".into(),
            })?;
        let record = Record::new(key, value).map_err(|error| StoreError::Migration {
            line,
            message: error.to_string(),
        })?;
        if records.insert(record.key().to_owned(), record).is_some() {
            return Err(StoreError::Migration {
                line,
                message: format!("duplicate key {key:?}"),
            });
        }
    }

    destination.initialize_records(records.into_values().collect())
}
