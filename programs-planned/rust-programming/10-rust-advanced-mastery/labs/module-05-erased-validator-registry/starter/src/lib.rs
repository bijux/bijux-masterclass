#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Record {
    pub key: String,
    pub value: String,
}

pub trait Validator {
    fn name(&self) -> &'static str;
    fn validate(&self, record: &Record) -> Result<(), String>;
}

pub struct NonEmptyKey;

impl Validator for NonEmptyKey {
    fn name(&self) -> &'static str {
        "non-empty-key"
    }

    fn validate(&self, record: &Record) -> Result<(), String> {
        if record.key.is_empty() {
            Err("key is empty".into())
        } else {
            Ok(())
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_validator_has_stable_identity() {
        assert_eq!(NonEmptyKey.name(), "non-empty-key");
    }
}
