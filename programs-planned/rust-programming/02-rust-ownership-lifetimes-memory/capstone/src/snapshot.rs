use crate::DocumentHandle;
use std::rc::{Rc, Weak};

/// Identity of an immutable document snapshot.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct SnapshotKey {
    /// Logical document identity.
    pub handle: DocumentHandle,
    /// Exact document revision copied into the snapshot.
    pub revision: u64,
}

/// Immutable, independently owned document state.
#[derive(Debug, PartialEq, Eq)]
pub struct DocumentSnapshot {
    key: SnapshotKey,
    title: Box<str>,
    text: Box<str>,
    tags: Box<[Box<str>]>,
}

impl DocumentSnapshot {
    pub(crate) fn new(
        handle: DocumentHandle,
        revision: u64,
        title: &str,
        text: &str,
        tags: &[String],
    ) -> Self {
        let tags = tags
            .iter()
            .map(|tag| tag.clone().into_boxed_str())
            .collect::<Vec<_>>()
            .into_boxed_slice();

        Self {
            key: SnapshotKey { handle, revision },
            title: title.to_owned().into_boxed_str(),
            text: text.to_owned().into_boxed_str(),
            tags,
        }
    }

    /// Return the document and revision represented by this snapshot.
    pub const fn key(&self) -> SnapshotKey {
        self.key
    }

    /// Borrow the snapshotted title.
    pub fn title(&self) -> &str {
        &self.title
    }

    /// Borrow the snapshotted text.
    pub fn text(&self) -> &str {
        &self.text
    }

    /// Borrow the snapshotted tags.
    pub fn tags(&self) -> &[Box<str>] {
        &self.tags
    }

    /// Return semantic UTF-8 payload bytes, excluding allocation overhead.
    pub fn payload_bytes(&self) -> usize {
        self.title.len()
            + self.text.len()
            + self.tags.iter().map(|tag| tag.len()).sum::<usize>()
    }
}

/// A non-owning observer of one snapshot allocation.
#[derive(Debug, Clone)]
pub struct SnapshotWatcher {
    key: SnapshotKey,
    weak: Weak<DocumentSnapshot>,
}

impl SnapshotWatcher {
    /// Create a weak observer without extending snapshot liveness.
    pub fn new(snapshot: &Rc<DocumentSnapshot>) -> Self {
        Self {
            key: snapshot.key(),
            weak: Rc::downgrade(snapshot),
        }
    }

    /// Return the key that was observed when this watcher was created.
    pub const fn key(&self) -> SnapshotKey {
        self.key
    }

    /// Attempt to acquire a strong owner of the snapshot.
    pub fn upgrade(&self) -> Option<Rc<DocumentSnapshot>> {
        self.weak.upgrade()
    }

    /// Report whether the allocation was alive during this call.
    ///
    /// This is only a momentary observation. Code that needs to use the
    /// snapshot should call [`Self::upgrade`] and keep the returned `Rc`.
    pub fn is_alive(&self) -> bool {
        self.upgrade().is_some()
    }
}
