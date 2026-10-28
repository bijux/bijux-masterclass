use crate::StoreError;

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct Record {
    key: String,
    value: String,
}

impl Record {
    pub fn new(
        key: impl Into<String>,
        value: impl Into<String>,
    ) -> Result<Self, StoreError> {
        let key = key.into();
        let value = value.into();
        validate_record_parts(&key, &value)?;
        Ok(Self { key, value })
    }

    pub fn key(&self) -> &str {
        &self.key
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

pub(crate) fn validate_key(key: &str) -> Result<(), StoreError> {
    validate_component("key", key, false)
}

pub(crate) fn validate_record_parts(
    key: &str,
    value: &str,
) -> Result<(), StoreError> {
    validate_key(key)?;
    validate_component("value", value, true)
}

fn validate_component(
    label: &str,
    value: &str,
    empty_allowed: bool,
) -> Result<(), StoreError> {
    if !empty_allowed && value.is_empty() {
        return Err(StoreError::InvalidRecord(format!(
            "{label} must not be empty"
        )));
    }
    if value
        .bytes()
        .any(|byte| matches!(byte, b'\t' | b'\r' | b'\n' | 0))
    {
        return Err(StoreError::InvalidRecord(format!(
            "{label} contains a forbidden control character"
        )));
    }
    Ok(())
}
