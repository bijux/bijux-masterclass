#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Record {
    pub key: String,
    pub value: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ValidationFailure {
    pub validator: &'static str,
    pub message: String,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum RegisterError {
    DuplicateName(&'static str),
}

pub trait Validator {
    fn name(&self) -> &'static str;
    fn validate(&self, record: &Record) -> Result<(), String>;
}

#[derive(Default)]
pub struct Registry {
    entries: Vec<Box<dyn Validator>>,
}

impl Registry {
    pub fn register<V>(&mut self, validator: V) -> Result<(), RegisterError>
    where
        V: Validator + 'static,
    {
        let name = validator.name();
        if self.entries.iter().any(|existing| existing.name() == name) {
            return Err(RegisterError::DuplicateName(name));
        }
        self.entries.push(Box::new(validator));
        Ok(())
    }

    pub fn validate(&self, record: &Record) -> Result<(), ValidationFailure> {
        for validator in &self.entries {
            validator
                .validate(record)
                .map_err(|message| ValidationFailure {
                    validator: validator.name(),
                    message,
                })?;
        }
        Ok(())
    }

    pub fn names(&self) -> impl Iterator<Item = &'static str> + '_ {
        self.entries.iter().map(|validator| validator.name())
    }
}

pub struct MaxValueLength(pub usize);

impl Validator for MaxValueLength {
    fn name(&self) -> &'static str {
        "max-value-length"
    }

    fn validate(&self, record: &Record) -> Result<(), String> {
        if record.value.len() > self.0 {
            Err(format!(
                "value length {} exceeds {}",
                record.value.len(),
                self.0
            ))
        } else {
            Ok(())
        }
    }
}

pub struct KeyPrefix(pub &'static str);

impl Validator for KeyPrefix {
    fn name(&self) -> &'static str {
        "key-prefix"
    }

    fn validate(&self, record: &Record) -> Result<(), String> {
        if record.key.starts_with(self.0) {
            Ok(())
        } else {
            Err(format!("key must begin with {:?}", self.0))
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn order_and_failure_identity_are_deterministic() {
        let mut registry = Registry::default();
        registry.register(KeyPrefix("cfg.")).expect("unique name");
        registry
            .register(MaxValueLength(3))
            .expect("unique name");

        assert_eq!(
            registry.names().collect::<Vec<_>>(),
            ["key-prefix", "max-value-length"]
        );

        let error = registry
            .validate(&Record {
                key: "cfg.name".into(),
                value: "long".into(),
            })
            .expect_err("value should be rejected");
        assert_eq!(error.validator, "max-value-length");
    }

    #[test]
    fn duplicate_name_does_not_change_the_registry() {
        let mut registry = Registry::default();
        registry
            .register(MaxValueLength(2))
            .expect("first registration");
        assert_eq!(
            registry.register(MaxValueLength(4)),
            Err(RegisterError::DuplicateName("max-value-length"))
        );
        assert_eq!(registry.names().count(), 1);
    }
}
