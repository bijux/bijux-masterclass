
//! FrameVault: a small systems-programming capstone.
//!
//! The crate separates safe binary parsing, domain invariants, operating-system
//! boundaries, one audited manual-allocation owner, and a panic-contained C ABI.

pub mod aligned;
pub mod app;
pub mod checksum;
pub mod codec;
pub mod domain;
pub mod error;
pub mod ffi;
pub mod path_policy;
pub mod process_capture;
pub mod store;

pub use codec::{DecodeError, DecodeErrorKind, EncodeError, Limits, decode, encode};
pub use domain::{Archive, ArchiveError, Entry, EntryKind, LogicalPath, LogicalPathError};
