//! Scoped access to one reusable normalization buffer.

#[derive(Debug, Default)]
pub struct ScopedText { scratch: String }

impl ScopedText {
    pub fn new() -> Self { Self::default() }

    pub fn with_normalized<R>(
        &mut self,
        raw: &str,
        operation: impl for<'view> FnOnce(&'view str) -> R,
    ) -> R {
        self.normalize(raw);
        operation(self.scratch.as_str())
    }

    pub fn visit_words<F>(&mut self, raw: &str, mut visitor: F)
    where
        F: for<'word> FnMut(&'word str),
    {
        self.normalize(raw);
        for word in self.scratch.split_whitespace() { visitor(word); }
    }

    pub fn capacity(&self) -> usize { self.scratch.capacity() }

    fn normalize(&mut self, raw: &str) {
        self.scratch.clear();
        let mut first = true;
        for word in raw.split_whitespace() {
            if !first { self.scratch.push(' '); }
            first = false;
            for character in word.chars() { self.scratch.extend(character.to_lowercase()); }
        }
    }
}

/// A normalized view cannot be retained outside the callback.
///
/// ```compile_fail
/// use rust_olm_lab_03_scoped_visitors::ScopedText;
/// let mut text = ScopedText::new();
/// let escaped: &str = text.with_normalized(" Hello ", |view| view);
/// println!("{escaped}");
/// ```
pub fn escape_prevention_contract() {}

#[cfg(test)]
mod tests {
    use super::*;
    use std::panic::{catch_unwind, AssertUnwindSafe};

    #[test]
    fn normalizes_unicode_and_whitespace() {
        let mut text = ScopedText::new();
        let value = text.with_normalized("  İSTANBUL\tRust  ", str::to_owned);
        assert_eq!(value, "i\u{307}stanbul rust");
    }

    #[test]
    fn owned_summaries_escape() {
        let mut text = ScopedText::new();
        let mut lengths = Vec::new();
        text.visit_words("one two", |word| lengths.push(word.len()));
        assert_eq!(lengths, [3, 3]);
    }

    #[test]
    fn scratch_is_reusable_after_callback_panic() {
        let mut text = ScopedText::new();
        let result = catch_unwind(AssertUnwindSafe(|| {
            text.with_normalized("before", |_| panic!("intentional"));
        }));
        assert!(result.is_err());
        let after = text.with_normalized(" AFTER ", str::to_owned);
        assert_eq!(after, "after");
    }

    #[test]
    fn repeated_calls_can_reuse_capacity() {
        let mut text = ScopedText::new();
        text.with_normalized("a considerably longer input", |_| ());
        let capacity = text.capacity();
        text.with_normalized("x", |_| ());
        assert!(text.capacity() >= capacity);
    }
}
