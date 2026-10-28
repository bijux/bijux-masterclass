//! Ownership-oriented in-memory document workspace.
//!
//! This Course 2 capstone integrates generational identities, borrowed views,
//! failure-atomic staged edits, bounded `Rc` snapshot retention, `Weak`
//! observation, revisioned interior caches, scoped `Cow` normalization, and
//! explicitly limited memory accounting. It uses safe Rust and the standard
//! library only.

mod cache;
mod edit;
mod handle;
mod memory;
mod model;
mod query;
mod script;
mod snapshot;
mod workspace;

pub use edit::EditSession;
pub use handle::{DocumentHandle, HandleBuildError, ParseHandleError};
pub use memory::{MemoryReport, TypeObservation};
pub use model::{CacheStats, DocumentView, MatchView, RemovedDocument};
pub use query::with_normalized_query;
pub use script::{ScriptEngine, ScriptError};
pub use snapshot::{DocumentSnapshot, SnapshotKey, SnapshotWatcher};
pub use workspace::{
    CommitFailure, CommitReceipt, Workspace, WorkspaceError, DEFAULT_SNAPSHOT_LIMIT,
};
