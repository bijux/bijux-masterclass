//! Reusable owned-buffer baseline for the scoped-visitors laboratory.
//!
//! This implementation returns an owned clone. Replacing that ownership escape
//! with a higher-ranked temporary view is the central laboratory task.

/// Reusable text scratch owner.
#[derive(Debug, Default)]
pub struct ScopedText {
    scratch: String,
}

impl ScopedText {
    /// Creates an empty scratch buffer.
    pub fn new() -> Self {
        Self::default()
    }

    /// Normalizes into reusable storage, then clones the result for the caller.
    pub fn normalize_owned(&mut self, raw: &str) -> String {
        self.scratch.clear();
        let mut pending_space = false;
        for character in raw.chars() {
            if character.is_whitespace() {
                pending_space = !self.scratch.is_empty();
            } else {
                if pending_space {
                    self.scratch.push(' ');
                    pending_space = false;
                }
                self.scratch.push(character);
            }
        }
        self.scratch.clone()
    }

    /// Returns current reusable capacity as an optimization observation.
    pub fn capacity(&self) -> usize {
        self.scratch.capacity()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_is_safe_but_allocates_an_escaping_owner() {
        let mut text = ScopedText::new();
        assert_eq!(text.normalize_owned("  Rust\tborrows  "), "Rust borrows");
        assert!(text.capacity() >= "Rust borrows".len());
    }
}
