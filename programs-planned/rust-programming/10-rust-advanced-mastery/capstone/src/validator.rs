use crate::{Record, StoreError};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ValidationIssue {
    code: &'static str,
    message: String,
}

impl ValidationIssue {
    pub fn new(code: &'static str, message: impl Into<String>) -> Self {
        Self {
            code,
            message: message.into(),
        }
    }

    pub fn code(&self) -> &'static str {
        self.code
    }

    pub fn message(&self) -> &str {
        &self.message
    }
}

pub trait Validator {
    fn name(&self) -> &'static str;
    fn validate(&self, record: &Record) -> Result<(), ValidationIssue>;
}

#[derive(Default)]
pub struct ValidatorRegistry {
    entries: Vec<Box<dyn Validator>>,
}

impl ValidatorRegistry {
    pub fn register<V>(&mut self, validator: V) -> Result<(), StoreError>
    where
        V: Validator + 'static,
    {
        let name = validator.name();
        if self.entries.iter().any(|current| current.name() == name) {
            return Err(StoreError::DuplicateValidator(name));
        }
        self.entries.push(Box::new(validator));
        Ok(())
    }

    pub fn validate(&self, record: &Record) -> Result<(), StoreError> {
        for validator in &self.entries {
            validator
                .validate(record)
                .map_err(|issue| StoreError::Validation {
                    validator: validator.name(),
                    code: issue.code(),
                    message: issue.message().to_owned(),
                })?;
        }
        Ok(())
    }

    pub fn names(&self) -> impl Iterator<Item = &'static str> + '_ {
        self.entries.iter().map(|entry| entry.name())
    }
}

pub struct MaxValueBytes(pub usize);

impl Validator for MaxValueBytes {
    fn name(&self) -> &'static str {
        "max-value-bytes"
    }

    fn validate(&self, record: &Record) -> Result<(), ValidationIssue> {
        if record.value().len() > self.0 {
            Err(ValidationIssue::new(
                "value-too-large",
                format!(
                    "value has {} bytes; limit is {}",
                    record.value().len(),
                    self.0
                ),
            ))
        } else {
            Ok(())
        }
    }
}

pub struct ReservedPrefix(pub &'static str);

impl Validator for ReservedPrefix {
    fn name(&self) -> &'static str {
        "reserved-prefix"
    }

    fn validate(&self, record: &Record) -> Result<(), ValidationIssue> {
        if record.key().starts_with(self.0) {
            Err(ValidationIssue::new(
                "reserved-key-prefix",
                format!("key uses reserved prefix {:?}", self.0),
            ))
        } else {
            Ok(())
        }
    }
}
