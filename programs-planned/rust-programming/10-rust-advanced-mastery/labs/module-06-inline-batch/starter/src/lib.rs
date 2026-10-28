pub struct SafeBatch<T, const N: usize> {
    values: Vec<T>,
}

impl<T, const N: usize> SafeBatch<T, N> {
    pub fn new() -> Self {
        Self {
            values: Vec::with_capacity(N),
        }
    }

    pub fn push(&mut self, value: T) -> Result<(), T> {
        if self.values.len() == N {
            Err(value)
        } else {
            self.values.push(value);
            Ok(())
        }
    }

    pub fn as_slice(&self) -> &[T] {
        &self.values
    }
}

impl<T, const N: usize> Default for SafeBatch<T, N> {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_oracle_enforces_capacity() {
        let mut batch = SafeBatch::<u8, 1>::new();
        assert_eq!(batch.push(1), Ok(()));
        assert_eq!(batch.push(2), Err(2));
    }
}
