use crate::edit::EditSession;
use crate::model::{
    Document, DocumentView, MatchView, RemovedDocument
};
use crate::query::with_normalized_query;
use crate::snapshot::{
    DocumentSnapshot, SnapshotKey
};
use crate::DocumentHandle;
use std::collections::{
    HashMap, HashSet, VecDeque
};
use std::fmt;
use std::num::NonZeroU64;
use std::rc::Rc;
/// Default maximum number of snapshots retained by a workspace.
pub const DEFAULT_SNAPSHOT_LIMIT: usize = 64;
#[derive(Debug)]
pub(crate) struct Slot {
    pub(crate) generation: NonZeroU64,
    pub(crate) document: Option<Document>,
}
/// A single-threaded in-memory document workspace.
///
/// Live documents are owned by generational slots. Immutable snapshots are
/// retained by a bounded first-in, first-out cache. External `Rc` owners may
/// keep an evicted snapshot alive independently of the workspace.
#[derive(Debug)]
pub struct Workspace {
    pub(crate) slots: Vec<Slot>,
    pub(crate) snapshots: HashMap<SnapshotKey, Rc<DocumentSnapshot>>,
    snapshot_order: VecDeque<SnapshotKey>,
    snapshot_limit: usize,
}
impl Default for Workspace {
    fn default() -> Self {
        Self::with_snapshot_limit(DEFAULT_SNAPSHOT_LIMIT)
    }
}
/// A domain or identity failure produced by workspace operations.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum WorkspaceError {
    /// No slot has ever existed at the requested index.
    UnknownSlot(usize),
    /// The requested slot exists but currently contains no document.
    VacantSlot(usize),
    /// The slot exists, but the handle names an older generation.
    StaleHandle {
        /// Rejected handle.
        handle: DocumentHandle,
        /// Generation currently associated with the slot.
        current_generation: u64,
    },
    /// A title was empty after trimming or contained a tab or line separator.
    InvalidTitle,
    /// A tag was empty, duplicated, or contained a tab or line separator.
    InvalidTag(String),
    /// An optimistic edit was based on a revision that is no longer current.
    RevisionConflict {
        /// Document targeted by the edit.
        handle: DocumentHandle,
        /// Revision captured when the session began.
        expected: u64,
        /// Revision currently stored in the workspace.
        actual: u64,
    },
    /// The revision counter could not be advanced.
    RevisionOverflow(DocumentHandle),
    /// The slot generation could not be advanced safely.
    GenerationOverflow(DocumentHandle),
}
impl fmt::Display for WorkspaceError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnknownSlot(slot) => write!(formatter, "unknown document slot {slot}"),
            Self::VacantSlot(slot) => write!(formatter, "document slot {slot} is vacant"),
            Self::StaleHandle {
                handle,
                current_generation,
            }
            => write!(
            formatter,
            "stale handle {handle}; slot generation is {current_generation}"
            ),
            Self::InvalidTitle => write!(
            formatter,
            "title must contain a non-whitespace character and no tab or line separator"
            ),
            Self::InvalidTag(tag) => write!(formatter, "invalid tag {tag:?}"),
            Self::RevisionConflict {
                handle,
                expected,
                actual,
            }
            => write!(
            formatter,
            "revision conflict for {handle}: expected {expected}, actual {actual}"
            ),
            Self::RevisionOverflow(handle) => {
                write!(formatter, "revision exhausted for {handle}")
            }
            Self::GenerationOverflow(handle) => {
                write!(formatter, "generation exhausted for {handle}")
            }
        }
    }
}
impl std::error::Error for WorkspaceError {
}
/// Successful result of committing an edit session.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CommitReceipt {
    /// Document that changed.
    pub handle: DocumentHandle,
    /// New live revision.
    pub revision: u64,
}
/// Failed commit plus the still-owned candidate session.
///
/// Returning the session lets the caller inspect, repair, retry, or discard the
/// candidate without reconstructing it from partially moved fields.
#[derive(Debug)]
pub struct CommitFailure {
    /// Reason the commit was rejected.
    pub error: WorkspaceError,
    /// Candidate state that was not installed.
    pub session: EditSession,
}
impl fmt::Display for CommitFailure {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.error.fmt(formatter)
    }
}
impl std::error::Error for CommitFailure {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.error)
    }
}
impl Workspace {
    /// Create an empty workspace with the default bounded snapshot cache.
    pub fn new() -> Self {
        Self::default()
    }
    /// Create an empty workspace with an explicit snapshot retention limit.
    ///
    /// A limit of zero disables workspace retention. `snapshot` still returns
    /// an external `Rc`, but a later request constructs a new allocation.
    pub fn with_snapshot_limit(snapshot_limit: usize) -> Self {
        Self {
            slots: Vec::new(),
            snapshots: HashMap::new(),
            snapshot_order: VecDeque::new(),
            snapshot_limit,
        }
    }
    /// Return the configured snapshot retention limit.
    pub const fn snapshot_limit(&self) -> usize {
        self.snapshot_limit
    }
    /// Return the number of snapshots currently retained by the workspace.
    pub fn retained_snapshot_count(&self) -> usize {
        self.snapshots.len()
    }
    /// Change the snapshot limit and immediately evict oldest retained entries.
    pub fn set_snapshot_limit(&mut self, snapshot_limit: usize) {
        self.snapshot_limit = snapshot_limit;
        self.enforce_snapshot_limit();
    }
    /// Drop all strong snapshot owners held by the workspace.
    pub fn clear_snapshot_cache(&mut self) {
        self.snapshots.clear();
        self.snapshot_order.clear();
    }
    /// Add a document with no tags.
    pub fn add(
    &mut self,
    title: impl Into<String>,
    text: impl Into<String>,
    ) -> Result<DocumentHandle, WorkspaceError> {
        self.add_with_tags(title, text, Vec::new())
    }
    /// Add a document after validating title and tag invariants.
    pub fn add_with_tags(
    &mut self,
    title: impl Into<String>,
    text: impl Into<String>,
    tags: Vec<String>,
    ) -> Result<DocumentHandle, WorkspaceError> {
        let title = title.into();
        validate_title(&title)?;
        validate_tags(&tags)?;
        let document = Document::new(title, text.into(), tags);
        if let Some((slot_index, slot)) = self
        .slots
        .iter_mut()
        .enumerate()
        .find(|(_, slot)| slot.document.is_none() && slot.generation.get() != u64::MAX)
        {
            slot.document = Some(document);
            return Ok(DocumentHandle::from_nonzero(slot_index, slot.generation));
        }
        let generation = NonZeroU64::MIN;
        let handle = DocumentHandle::from_nonzero(self.slots.len(), generation);
        self.slots.push(Slot {
            generation,
            document: Some(document),
        });
        Ok(handle)
    }
    /// Borrow an immutable view of a live document.
    pub fn view(&self, handle: DocumentHandle) -> Result<DocumentView<'_>, WorkspaceError> {
        Ok(self.resolve(handle)?.view(handle))
    }
    /// Borrow one zero-based logical line from a live document.
    pub fn line(
    &self,
    handle: DocumentHandle,
    index: usize,
    ) -> Result<Option<&str>, WorkspaceError> {
        Ok(self.resolve(handle)?.line(index))
    }
    /// Create an owned edit session from the current document revision.
    pub fn begin_edit(&self, handle: DocumentHandle) -> Result<EditSession, WorkspaceError> {
        let document = self.resolve(handle)?;
        Ok(EditSession::new(
        handle,
        document.revision,
        document.title.clone(),
        document.text.clone(),
        document.tags.clone(),
        ))
    }
    /// Validate and install an edit session atomically with respect to this API.
    ///
    /// On every error path the live document is unchanged and the rejected
    /// session is returned inside [`CommitFailure`].
    pub fn commit(&mut self, session: EditSession) -> Result<CommitReceipt, CommitFailure> {
        if let Err(error) = validate_title(&session.title).and_then(|()| validate_tags(&session.tags)) {
            return Err(CommitFailure {
                error, session
            });
        }
        let document = match self.resolve_mut(session.handle) {
            Ok(document) => document,
            Err(error) => return Err(CommitFailure {
                error, session
            }),
        };
        if document.revision != session.expected_revision {
            let error = WorkspaceError::RevisionConflict {
                handle: session.handle,
                expected: session.expected_revision,
                actual: document.revision,
            };
            return Err(CommitFailure {
                error, session
            });
        }
        let next_revision = match document.revision.checked_add(1) {
            Some(value) => value,
            None => {
                return Err(CommitFailure {
                    error: WorkspaceError::RevisionOverflow(session.handle),
                    session,
                });
            }
        };
        document.title = session.title;
        document.text = session.text;
        document.tags = session.tags;
        document.revision = next_revision;
        document.invalidate_cache();
        Ok(CommitReceipt {
            handle: session.handle,
            revision: next_revision,
        })
    }
    /// Remove a document and invalidate all handles to its old generation.
    pub fn remove(
    &mut self,
    handle: DocumentHandle,
    ) -> Result<RemovedDocument, WorkspaceError> {
        let slot = self.slot_mut(handle)?;
        if slot.document.is_none() {
            return Err(WorkspaceError::VacantSlot(handle.slot()));
        }
        let next_generation = slot
        .generation
        .get()
        .checked_add(1)
        .and_then(NonZeroU64::new)
        .ok_or(WorkspaceError::GenerationOverflow(handle))?;
        let document = slot
        .document
        .take()
        .ok_or(WorkspaceError::VacantSlot(handle.slot()))?;
        slot.generation = next_generation;
        Ok(document.into())
    }
    /// Search live document text for a normalized, case-sensitive byte substring.
    ///
    /// Query whitespace is trimmed and collapsed. Document text is not
    /// normalized. Matches therefore borrow exact UTF-8 substrings from live
    /// document storage and their ranges are byte ranges, not character indices.
    pub fn search(&self, raw_query: &str) -> Vec<MatchView<'_>> {
        with_normalized_query(raw_query, |query| self.search_normalized(query))
    }
    fn search_normalized(&self, query: &str) -> Vec<MatchView<'_>> {
        if query.is_empty() {
            return Vec::new();
        }
        let mut matches = Vec::new();
        for (slot_index, slot) in self.slots.iter().enumerate() {
            let Some(document) = slot.document.as_ref() else {
                continue;
            };
            let handle = DocumentHandle::from_nonzero(slot_index, slot.generation);
            for (start, matched) in document.text.match_indices(query) {
                let range = start..start + matched.len();
                matches.push(MatchView {
                    handle,
                    revision: document.revision,
                    title: &document.title,
                    matched,
                    line: document.line_number_at(start),
                    range,
                });
            }
        }
        matches
    }
    /// Return a shared immutable snapshot of the document's current revision.
    ///
    /// Repeated requests share one allocation while the key remains in the
    /// bounded workspace cache. FIFO eviction removes only the workspace's
    /// strong owner; external `Rc` owners remain valid.
    pub fn snapshot(
    &mut self,
    handle: DocumentHandle,
    ) -> Result<Rc<DocumentSnapshot>, WorkspaceError> {
        let revision = self.resolve(handle)?.revision;
        let key = SnapshotKey {
            handle, revision
        };
        if let Some(existing) = self.snapshots.get(&key) {
            return Ok(Rc::clone(existing));
        }
        let snapshot = {
            let document = self.resolve(handle)?;
            Rc::new(DocumentSnapshot::new(
            handle,
            document.revision,
            &document.title,
            &document.text,
            &document.tags,
            ))
        };
        if self.snapshot_limit > 0 {
            self.snapshots.insert(key, Rc::clone(&snapshot));
            self.snapshot_order.push_back(key);
            self.enforce_snapshot_limit();
        }
        Ok(snapshot)
    }
    /// Remove one snapshot key from workspace retention.
    pub fn evict_snapshot(&mut self, key: SnapshotKey) -> bool {
        let removed = self.snapshots.remove(&key).is_some();
        if removed {
            self.snapshot_order.retain(|candidate| *candidate != key);
        }
        removed
    }
    /// Return cache hit and miss counters for one live document.
    pub fn cache_stats(&self, handle: DocumentHandle) -> Result<crate::CacheStats, WorkspaceError> {
        Ok(self.resolve(handle)?.cache_stats())
    }
    /// Return all currently live handles in slot order.
    pub fn handles(&self) -> Vec<DocumentHandle> {
        self.slots
        .iter()
        .enumerate()
        .filter_map(|(index, slot)| {
            slot.document
            .as_ref()
            .map(|_| DocumentHandle::from_nonzero(index, slot.generation))
        })
        .collect()
    }
    fn enforce_snapshot_limit(&mut self) {
        while self.snapshots.len() > self.snapshot_limit {
            let Some(oldest) = self.snapshot_order.pop_front() else {
                break;
            };
            self.snapshots.remove(&oldest);
        }
    }
    fn resolve(&self, handle: DocumentHandle) -> Result<&Document, WorkspaceError> {
        let slot = self.slot(handle)?;
        slot.document
        .as_ref()
        .ok_or(WorkspaceError::VacantSlot(handle.slot()))
    }
    fn resolve_mut(&mut self, handle: DocumentHandle) -> Result<&mut Document, WorkspaceError> {
        let slot = self.slot_mut(handle)?;
        slot.document
        .as_mut()
        .ok_or(WorkspaceError::VacantSlot(handle.slot()))
    }
    fn slot(&self, handle: DocumentHandle) -> Result<&Slot, WorkspaceError> {
        let slot = self
        .slots
        .get(handle.slot())
        .ok_or(WorkspaceError::UnknownSlot(handle.slot()))?;
        if slot.generation.get() != handle.generation() {
            return Err(WorkspaceError::StaleHandle {
                handle,
                current_generation: slot.generation.get(),
            });
        }
        Ok(slot)
    }
    fn slot_mut(&mut self, handle: DocumentHandle) -> Result<&mut Slot, WorkspaceError> {
        let slot = self
        .slots
        .get_mut(handle.slot())
        .ok_or(WorkspaceError::UnknownSlot(handle.slot()))?;
        if slot.generation.get() != handle.generation() {
            return Err(WorkspaceError::StaleHandle {
                handle,
                current_generation: slot.generation.get(),
            });
        }
        Ok(slot)
    }
}
fn validate_title(title: &str) -> Result<(), WorkspaceError> {
    if title.trim().is_empty()
    || title.contains(|character: char| matches!(character, '\n' | '\r' | '\t'))
    {
        Err(WorkspaceError::InvalidTitle)
    }
    else {
        Ok(())
    }
}
fn validate_tags(tags: &[String]) -> Result<(), WorkspaceError> {
    let mut seen = HashSet::new();
    for tag in tags {
        if tag.trim().is_empty()
        || tag.contains(|character: char| matches!(character, '\n' | '\r' | '\t'))
        || !seen.insert(tag.as_str())
        {
            return Err(WorkspaceError::InvalidTag(tag.clone()));
        }
    }
    Ok(())
}
