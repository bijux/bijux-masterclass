//! Revision-aware line cache with private interior mutability.
use std::cell::{
    Cell, RefCell
};
use std::fmt;
use std::ops::Range;
#[derive(Debug, Clone, PartialEq, Eq)]
struct Cache {
    revision: u64, lines: Vec<Range<usize>>
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CacheStats {
    pub hits: u64, pub misses: u64
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CacheBusy;
impl fmt::Display for CacheBusy {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "cache is already borrowed")
    }
}
impl std::error::Error for CacheBusy {
}
#[derive(Debug)]
pub struct IndexedText {
    text: String,
    revision: u64,
    cache: RefCell<Option<Cache>>,
    hits: Cell<u64>,
    misses: Cell<u64>,
}
impl IndexedText {
    pub fn new(text: impl Into<String>) -> Self {
        Self {
            text: text.into(), revision: 0, cache: RefCell::new(None), hits: Cell::new(0), misses: Cell::new(0)
        }
    }
    pub fn text(&self) -> &str {
        &self.text
    }
    pub fn revision(&self) -> u64 {
        self.revision
    }
    pub fn stats(&self) -> CacheStats {
        CacheStats {
            hits: self.hits.get(), misses: self.misses.get()
        }
    }
    pub fn try_line(&self, index: usize) -> Result<Option<&str>, CacheBusy> {
        let range = self.try_line_range(index)?;
        Ok(range.map(|range| &self.text[range]))
    }
    pub fn append(&mut self, suffix: &str) -> Result<(), &'static str> {
        let next = self.revision.checked_add(1).ok_or("revision overflow")?;
        self.text.push_str(suffix);
        self.revision = next;
        self.cache.get_mut().take();
        Ok(())
    }
    pub fn replace(&mut self, text: String) -> Result<String, &'static str> {
        let next = self.revision.checked_add(1).ok_or("revision overflow")?;
        let old = std::mem::replace(&mut self.text, text);
        self.revision = next;
        self.cache.get_mut().take();
        Ok(old)
    }
    fn try_line_range(&self, index: usize) -> Result<Option<Range<usize>>, CacheBusy> {
        {
            let cache = self.cache.try_borrow().map_err(|_| CacheBusy)?;
            if let Some(cache) = cache.as_ref().filter(|cache| cache.revision == self.revision) {
                self.hits.set(self.hits.get().saturating_add(1));
                return Ok(cache.lines.get(index).cloned());
            }
        }
        let lines = line_ranges(&self.text);
        let answer = lines.get(index).cloned();
        let mut cache = self.cache.try_borrow_mut().map_err(|_| CacheBusy)?;
        *cache = Some(Cache {
            revision: self.revision, lines
        });
        self.misses.set(self.misses.get().saturating_add(1));
        Ok(answer)
    }
}
fn line_ranges(text: &str) -> Vec<Range<usize>> {
    if text.is_empty() {
        return Vec::new();
    }
    let mut ranges = Vec::new();
    let mut start = 0;
    for segment in text.split_inclusive('\n') {
        let without_newline = segment.strip_suffix('\n').unwrap_or(segment);
        let content = without_newline.strip_suffix('\r').unwrap_or(without_newline);
        ranges.push(start..start + content.len());
        start += segment.len();
    }
    ranges
}
impl PartialEq for IndexedText {
    fn eq(&self, other: &Self) -> bool {
        self.text == other.text && self.revision == other.revision
    }
}
impl Eq for IndexedText {
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn cold_then_hot_query_updates_diagnostics_only() {
        let text = IndexedText::new("alpha\nβeta");
        assert_eq!(text.try_line(1), Ok(Some("βeta")));
        assert_eq!(text.stats(), CacheStats {
            hits: 0, misses: 1
        });
        assert_eq!(text.try_line(0), Ok(Some("alpha")));
        assert_eq!(text.stats(), CacheStats {
            hits: 1, misses: 1
        });
    }
    #[test]
    fn mutation_invalidates_cache() {
        let mut text = IndexedText::new("a");
        assert_eq!(text.try_line(0), Ok(Some("a")));
        assert_eq!(text.append("\nb"), Ok(()));
        assert_eq!(text.try_line(1), Ok(Some("b")));
        assert_eq!(text.stats().misses, 2);
    }
    #[test]
    fn held_guard_becomes_domain_error_not_panic() {
        let text = IndexedText::new("a");
        let _guard = text.cache.borrow_mut();
        assert_eq!(text.try_line(0), Err(CacheBusy));
    }
    #[test]
    fn cache_does_not_affect_equality() {
        let left = IndexedText::new("a");
        let right = IndexedText::new("a");
        assert_eq!(left.try_line(0), Ok(Some("a")));
        assert_eq!(left, right);
    }
}
