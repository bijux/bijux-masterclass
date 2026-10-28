//! Runtime-only arena identity baseline.
//!
//! Plain indices from distinct arenas are type-confusable. Generative invariant
//! brands and negative compiler evidence remain the learner's work.

/// Unbranded runtime index.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Id(pub usize);

/// Arena checked only by runtime bounds.
#[derive(Debug, Default)]
pub struct Arena<T> {
    values: Vec<T>,
}

impl<T> Arena<T> {
    /// Inserts a value and returns an unbranded index.
    pub fn insert(&mut self, value: T) -> Id {
        let id = Id(self.values.len());
        self.values.push(value);
        id
    }

    /// Looks up an index with runtime bounds checking.
    pub fn get(&self, id: Id) -> Option<&T> {
        self.values.get(id.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_demonstrates_cross_arena_confusion() {
        let mut first = Arena::default();
        let mut second = Arena::default();
        let id = first.insert("first");
        second.insert("second");
        assert_eq!(second.get(id), Some(&"second"));
    }
}
