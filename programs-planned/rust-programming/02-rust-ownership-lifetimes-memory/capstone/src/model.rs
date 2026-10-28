use crate::cache::{line_ranges, DocumentCache};
use crate::DocumentHandle;
use std::cell::{Cell, RefCell};
use std::ops::Range;

/// Cumulative observations of the revisioned line cache.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CacheStats {
    /// Queries served by a cache built for the current document revision.
    pub hits: u64,
    /// Queries that had to rebuild a missing or stale cache.
    pub misses: u64,
}

#[derive(Debug)]
pub(crate) struct Document {
    pub(crate) title: String,
    pub(crate) text: String,
    pub(crate) tags: Vec<String>,
    pub(crate) revision: u64,
    pub(crate) cache: RefCell<Option<DocumentCache>>,
    pub(crate) cache_hits: Cell<u64>,
    pub(crate) cache_misses: Cell<u64>,
}

impl Document {
    pub(crate) fn new(title: String, text: String, tags: Vec<String>) -> Self {
        Self {
            title,
            text,
            tags,
            revision: 0,
            cache: RefCell::new(None),
            cache_hits: Cell::new(0),
            cache_misses: Cell::new(0),
        }
    }

    pub(crate) fn view(&self, handle: DocumentHandle) -> DocumentView<'_> {
        DocumentView {
            handle,
            title: &self.title,
            text: &self.text,
            tags: &self.tags,
            revision: self.revision,
        }
    }

    pub(crate) fn cache_stats(&self) -> CacheStats {
        CacheStats {
            hits: self.cache_hits.get(),
            misses: self.cache_misses.get(),
        }
    }

    pub(crate) fn line(&self, index: usize) -> Option<&str> {
        let range = self.line_range(index)?;
        Some(&self.text[range])
    }

    pub(crate) fn line_number_at(&self, byte: usize) -> Option<usize> {
        self.ensure_cache();
        let cache = self.cache.borrow();
        let cache = cache.as_ref()?;
        cache.lines.iter().position(|range| range.contains(&byte))
    }

    fn line_range(&self, index: usize) -> Option<Range<usize>> {
        self.ensure_cache();
        self.cache
            .borrow()
            .as_ref()
            .and_then(|cache| cache.lines.get(index).cloned())
    }

    fn ensure_cache(&self) {
        let hit = {
            let cache = self.cache.borrow();
            cache
                .as_ref()
                .is_some_and(|cache| cache.revision == self.revision)
        };

        if hit {
            self.cache_hits
                .set(self.cache_hits.get().saturating_add(1));
            return;
        }

        let lines = line_ranges(&self.text);
        *self.cache.borrow_mut() = Some(DocumentCache {
            revision: self.revision,
            lines,
        });
        self.cache_misses
            .set(self.cache_misses.get().saturating_add(1));
    }

    pub(crate) fn invalidate_cache(&mut self) {
        self.cache.get_mut().take();
    }
}

/// A borrowed, immutable projection of one live document.
///
/// The view cannot outlive the shared borrow of its workspace.
#[derive(Debug, Clone, Copy)]
pub struct DocumentView<'a> {
    handle: DocumentHandle,
    title: &'a str,
    text: &'a str,
    tags: &'a [String],
    revision: u64,
}

impl<'a> DocumentView<'a> {
    /// Return the logical identity of the viewed document.
    pub const fn handle(self) -> DocumentHandle {
        self.handle
    }

    /// Borrow the title.
    pub const fn title(self) -> &'a str {
        self.title
    }

    /// Borrow the text.
    pub const fn text(self) -> &'a str {
        self.text
    }

    /// Borrow the tags.
    pub const fn tags(self) -> &'a [String] {
        self.tags
    }

    /// Return the revision represented by this view.
    pub const fn revision(self) -> u64 {
        self.revision
    }
}

/// One borrowed substring match in a live document.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MatchView<'a> {
    /// Document containing the match.
    pub handle: DocumentHandle,
    /// Revision searched.
    pub revision: u64,
    /// Borrowed title of the matching document.
    pub title: &'a str,
    /// Borrowed matched substring.
    pub matched: &'a str,
    /// Byte range of the match within the document text.
    pub range: Range<usize>,
    /// Zero-based logical line containing the first matched byte.
    pub line: Option<usize>,
}

/// Owned document state returned by [`crate::Workspace::remove`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RemovedDocument {
    /// Removed title.
    pub title: String,
    /// Removed text.
    pub text: String,
    /// Removed tags.
    pub tags: Vec<String>,
    /// Final live revision before removal.
    pub revision: u64,
}

impl From<Document> for RemovedDocument {
    fn from(document: Document) -> Self {
        Self {
            title: document.title,
            text: document.text,
            tags: document.tags,
            revision: document.revision,
        }
    }
}
