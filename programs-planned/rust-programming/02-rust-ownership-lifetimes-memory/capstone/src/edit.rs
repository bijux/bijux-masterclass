use crate::DocumentHandle;

/// Owned candidate state for an optimistic document edit.
///
/// Creating a session clones the current document state. Mutating the session
/// therefore cannot alter the live workspace. [`crate::Workspace::commit`]
/// replaces live state only after validating the complete candidate and its
/// expected revision.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EditSession {
    pub(crate) handle: DocumentHandle,
    pub(crate) expected_revision: u64,
    pub(crate) title: String,
    pub(crate) text: String,
    pub(crate) tags: Vec<String>,
}

impl EditSession {
    pub(crate) fn new(
        handle: DocumentHandle,
        expected_revision: u64,
        title: String,
        text: String,
        tags: Vec<String>,
    ) -> Self {
        Self {
            handle,
            expected_revision,
            title,
            text,
            tags,
        }
    }

    /// Return the document targeted by this session.
    pub const fn handle(&self) -> DocumentHandle {
        self.handle
    }

    /// Return the revision that must still be live when this session commits.
    pub const fn expected_revision(&self) -> u64 {
        self.expected_revision
    }

    /// Borrow the candidate title.
    pub fn title(&self) -> &str {
        &self.title
    }

    /// Borrow the candidate text.
    pub fn text(&self) -> &str {
        &self.text
    }

    /// Borrow the candidate tags.
    pub fn tags(&self) -> &[String] {
        &self.tags
    }

    /// Replace the candidate title.
    pub fn set_title(&mut self, title: impl Into<String>) {
        self.title = title.into();
    }

    /// Replace the candidate text.
    pub fn set_text(&mut self, text: impl Into<String>) {
        self.text = text.into();
    }

    /// Add a tag unless the candidate already contains an identical tag.
    pub fn add_tag(&mut self, tag: impl Into<String>) {
        let tag = tag.into();
        if !self.tags.iter().any(|current| current == &tag) {
            self.tags.push(tag);
        }
    }

    /// Remove all occurrences of `tag`, returning whether the candidate changed.
    pub fn remove_tag(&mut self, tag: &str) -> bool {
        let before = self.tags.len();
        self.tags.retain(|current| current != tag);
        self.tags.len() != before
    }
}
