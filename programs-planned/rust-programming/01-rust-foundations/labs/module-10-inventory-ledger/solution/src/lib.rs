//! Persistent inventory ledger used as the independent Course 1 transfer proof.
//!
//! # Domain use
//!
//! ```
//! use rust_foundations_lab_10_inventory_ledger::{ItemState, Ledger};
//!
//! let mut ledger = Ledger::new();
//! let id = ledger.add(String::from("caliper")).expect("valid item");
//! ledger.checkout(id, String::from("Ada")).expect("available");
//! assert_eq!(
//!     ledger.find(id).map(|item| item.state()),
//!     Some(&ItemState::CheckedOut {
//!         borrower: String::from("Ada"),
//!     })
//! );
//! ```
//!
//! # Command parsing
//!
//! ```
//! use rust_foundations_lab_10_inventory_ledger::{Command, parse_command};
//!
//! let args = vec![
//!     String::from("checkout"),
//!     String::from("4"),
//!     String::from("Grace"),
//!     String::from("Hopper"),
//! ];
//! assert!(matches!(
//!     parse_command(&args),
//!     Ok(Command::Checkout { borrower, .. }) if borrower == "Grace Hopper"
//! ));
//! ```
//!
//! # Generic codec
//!
//! ```
//! use rust_foundations_lab_10_inventory_ledger::{Ledger, load_from, save_to};
//! use std::io::Cursor;
//!
//! let mut ledger = Ledger::new();
//! ledger.add(String::from("scope")).expect("valid");
//! let mut bytes = Vec::new();
//! save_to(&mut bytes, &ledger).expect("memory writer");
//! let restored = load_from(Cursor::new(bytes)).expect("memory reader");
//! assert_eq!(restored.items().len(), 1);
//! ```

mod application;
mod codec;
mod command;
mod domain;

pub use application::{Outcome, RunError, execute, run};
pub use codec::{RecordError, StorageError, load_from, load_path, save_to, save_path};
pub use command::{Command, CommandError, Filter, HELP, parse_command};
pub use domain::{Counts, DomainError, Item, ItemId, ItemState, Ledger, ParseItemIdError};
