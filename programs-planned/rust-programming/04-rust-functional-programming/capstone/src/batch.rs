#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Batch<T, E> {
    accepted: Vec<T>,
    rejected: Vec<E>,
}

impl<T, E> Default for Batch<T, E> {
    fn default() -> Self {
        Self {
            accepted: Vec::new(),
            rejected: Vec::new(),
        }
    }
}

impl<T, E> Batch<T, E> {
    pub fn accepted(&self) -> &[T] {
        &self.accepted
    }

    pub fn rejected(&self) -> &[E] {
        &self.rejected
    }

    pub fn into_parts(self) -> (Vec<T>, Vec<E>) {
        (self.accepted, self.rejected)
    }
}

impl<T, E> FromIterator<Result<T, E>> for Batch<T, E> {
    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = Result<T, E>>,
    {
        let mut batch = Self::default();
        batch.extend(iter);
        batch
    }
}

impl<T, E> Extend<Result<T, E>> for Batch<T, E> {
    fn extend<I>(&mut self, iter: I)
    where
        I: IntoIterator<Item = Result<T, E>>,
    {
        for item in iter {
            match item {
                Ok(value) => self.accepted.push(value),
                Err(error) => self.rejected.push(error),
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Batch;

    #[test]
    fn collection_preserves_order_within_each_channel() {
        let batch: Batch<u8, &str> = [Ok(1), Err("a"), Ok(2), Err("b")]
            .into_iter()
            .collect();
        assert_eq!(batch.accepted(), &[1, 2]);
        assert_eq!(batch.rejected(), &["a", "b"]);
    }
}
