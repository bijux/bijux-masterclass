//! AxiomStore is the synthesis capstone for Rust Advanced Mastery.
//!
//! The public surface intentionally exposes stable owned records, immutable
//! snapshots, lending record traversal, bounded transactions, and runtime
//! validators while keeping representation-specific codecs and unsafe inline
//! storage private.

mod app;
mod domain;
mod error;
mod format;
mod inline_batch;
mod migration;
mod snapshot;
mod store;
mod validator;

pub use app::{help, run, SCHEMA, VERSION};
pub use domain::Record;
pub use error::StoreError;
pub use format::RecordView;
pub(crate) use inline_batch::InlineBatch;
pub use migration::migrate_v0;
pub use snapshot::{LendingRecords, RecordCursor, Snapshot};
pub use store::{Store, Transaction};
pub use validator::{
    MaxValueBytes, ReservedPrefix, ValidationIssue, Validator, ValidatorRegistry,
};

/// A compile-fail contract: a borrowed record view cannot outlive its snapshot.
///
/// ```compile_fail
/// use axiomstore::{LendingRecords, Store};
///
/// let escaped = {
///     let store = Store::<4096, 8>::new("example.ax").unwrap();
///     let snapshot = store.open_snapshot().unwrap();
///     let mut cursor = snapshot.records();
///     cursor.next().unwrap().unwrap()
/// };
/// println!("{}", escaped.key());
/// ```
pub struct BorrowContract;
