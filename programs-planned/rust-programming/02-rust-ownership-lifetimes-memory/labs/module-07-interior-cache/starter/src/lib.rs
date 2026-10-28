//! Ordinary-mutation baseline before derived-state interior mutability.

/// Editable text with no derived cache.
#[derive(Debug, Default, PartialEq, Eq)]
pub struct IndexedText {
    text: String,
}

impl IndexedText {
    /// Creates editable text.
    pub fn new(text: impl Into<String>) -> Self {
        Self { text: text.into() }
    }

    /// Borrows semantic text.
    pub fn text(&self) -> &str {
        &self.text
    }

    /// Mutates semantic state through ordinary exclusive access.
    pub fn append(&mut self, suffix: &str) {
        self.text.push_str(suffix);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_needs_no_interior_mutability() {
        let mut text = IndexedText::new("one");
        text.append("\ntwo");
        assert_eq!(text.text(), "one\ntwo");
    }
}
