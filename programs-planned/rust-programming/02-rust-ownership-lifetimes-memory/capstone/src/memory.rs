use crate::Workspace;
use std::mem::{
    align_of, size_of
};
use std::ops::Range;
use std::rc::Rc;
/// A target-conditioned size and alignment observation.
///
/// This value records what the compiled program observes on its current target.
/// It is not a portable layout guarantee unless the relevant Rust contract says
/// so independently.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TypeObservation {
    /// Human-readable type label.
    pub type_name: &'static str,
    /// `size_of::<T>()` on the current target.
    pub size: usize,
    /// `align_of::<T>()` on the current target.
    pub alignment: usize,
    /// Epistemic classification of this measurement.
    pub classification: &'static str,
}
/// A deliberately partial memory-accounting report.
///
/// Payload lengths and capacities are useful bounded observations of storage the
/// application directly controls. They are not an exact heap profile. See
/// [`Self::exclusions`] for categories intentionally omitted.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MemoryReport {
    /// Number of occupied document slots.
    pub live_documents: usize,
    /// Sum of live title UTF-8 lengths.
    pub title_payload_bytes: usize,
    /// Sum of live text UTF-8 lengths.
    pub text_payload_bytes: usize,
    /// Sum of live tag UTF-8 lengths.
    pub tag_payload_bytes: usize,
    /// Sum of `String` capacities owned by live document fields.
    pub live_string_capacity_bytes: usize,
    /// Number of cached line ranges currently stored.
    pub cached_line_ranges: usize,
    /// Capacity bytes of cached `Range<usize>` vectors.
    pub cached_line_range_capacity_bytes: usize,
    /// Number of snapshot keys strongly retained by the workspace.
    pub snapshot_cache_entries: usize,
    /// Configured upper bound for workspace-retained snapshot keys.
    pub snapshot_retention_limit: usize,
    /// Number of distinct snapshot allocations retained by the workspace.
    pub unique_snapshot_allocations: usize,
    /// Semantic UTF-8 payload bytes in distinct retained snapshots.
    pub unique_snapshot_payload_bytes: usize,
    /// Current-target observations for selected public types.
    pub observations: Vec<TypeObservation>,
    /// Categories excluded from this report.
    pub exclusions: &'static [&'static str],
}
impl MemoryReport {
    /// Sum semantic live-document payload bytes.
    pub const fn live_payload_bytes(&self) -> usize {
        self.title_payload_bytes + self.text_payload_bytes + self.tag_payload_bytes
    }
}
impl Workspace {
    /// Produce a bounded accounting report without claiming exact allocator use.
    pub fn memory_report(&self) -> MemoryReport {
        let documents = self
        .slots
        .iter()
        .filter_map(|slot| slot.document.as_ref())
        .collect::<Vec<_>>();
        let title_payload_bytes = documents.iter().map(|document| document.title.len()).sum();
        let text_payload_bytes = documents.iter().map(|document| document.text.len()).sum();
        let tag_payload_bytes = documents
        .iter()
        .flat_map(|document| document.tags.iter())
        .map(String::len)
        .sum();
        let live_string_capacity_bytes = documents
        .iter()
        .map(|document| {
            document.title.capacity()
            + document.text.capacity()
            + document
            .tags
            .iter()
            .map(String::capacity)
            .sum::<usize>()
        })
        .sum();
        let mut cached_line_ranges = 0;
        let mut cached_line_range_capacity_bytes = 0;
        for document in &documents {
            let cache = document.cache.borrow();
            if let Some(cache) = cache.as_ref() {
                cached_line_ranges += cache.lines.len();
                cached_line_range_capacity_bytes +=
                cache.lines.capacity() * size_of::<Range<usize>>();
            }
        }
        let mut unique: Vec<&Rc<crate::DocumentSnapshot>> = Vec::new();
        for snapshot in self.snapshots.values() {
            if !unique
            .iter()
            .any(|existing| Rc::ptr_eq(existing, snapshot))
            {
                unique.push(snapshot);
            }
        }
        let unique_snapshot_payload_bytes = unique
        .iter()
        .map(|snapshot| snapshot.payload_bytes())
        .sum();
        MemoryReport {
            live_documents: documents.len(),
            title_payload_bytes,
            text_payload_bytes,
            tag_payload_bytes,
            live_string_capacity_bytes,
            cached_line_ranges,
            cached_line_range_capacity_bytes,
            snapshot_cache_entries: self.snapshots.len(),
            snapshot_retention_limit: self.snapshot_limit(),
            unique_snapshot_allocations: unique.len(),
            unique_snapshot_payload_bytes,
            observations: vec![
            observe::<crate::DocumentHandle>("DocumentHandle"),
            observe::<String>("String owner"),
            observe::<Box<str>>("Box<str> owner"),
            observe::<Rc<crate::DocumentSnapshot>>("Rc<DocumentSnapshot> owner"),
            observe::<crate::EditSession>("EditSession"),
            ],
            exclusions: &[
            "allocator metadata and fragmentation",
            "HashMap and Vec control allocations not represented by explicit capacities",
            "Rc control-block bytes and weak-count bookkeeping",
            "stack frames and register state",
            "executable code and static data",
            "temporary formatting and parser allocations",
            "external Rc owners after workspace eviction",
            ],
        }
    }
}
fn observe<T>(type_name: &'static str) -> TypeObservation {
    TypeObservation {
        type_name,
        size: size_of::<T>(),
        alignment: align_of::<T>(),
        classification: "observed on current target and toolchain; not by itself a portable guarantee",
    }
}
