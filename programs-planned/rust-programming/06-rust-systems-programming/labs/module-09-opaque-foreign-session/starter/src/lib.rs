
#![forbid(unsafe_code)]

#[derive(Debug)]
pub struct Counter {
    value: i64,
}

impl Counter {
    #[must_use]
    pub const fn new(value: i64) -> Self {
        Self { value }
    }

    pub fn add(&mut self, delta: i64) -> Option<i64> {
        self.value = self.value.checked_add(delta)?;
        Some(self.value)
    }

    #[must_use]
    pub const fn get(&self) -> i64 {
        self.value
    }
}

#[cfg(test)]
mod tests {
    use super::Counter;

    #[test]
    fn safe_model_checks_overflow() {
        let mut counter = Counter::new(i64::MAX);
        assert_eq!(counter.add(1), None);
        assert_eq!(counter.get(), i64::MAX);
    }
}
