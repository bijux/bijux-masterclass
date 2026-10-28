//! A small registry used to demonstrate library, application, and process boundaries.
//!
//! The library owns domain rules. The binary owns process concerns.
//!
//! # Construct and mutate
//!
//! ```
//! use rust_foundations_lab_09_library_boundaries::Registry;
//!
//! let mut registry = Registry::new();
//! let id = registry.add(String::from("parser")).expect("valid label");
//! assert_eq!(registry.get(id).map(|entry| entry.label), Some("parser"));
//! ```
//!
//! # Parse a command
//!
//! ```
//! use rust_foundations_lab_09_library_boundaries::{parse_command, Command};
//!
//! let args = vec![String::from("add"), String::from("record"), String::from("parser")];
//! assert_eq!(parse_command(&args), Ok(Command::Add(String::from("record parser"))));
//! ```
//!
//! # Execute through the application boundary
//!
//! ```
//! use rust_foundations_lab_09_library_boundaries::{execute, Command, Registry};
//!
//! let mut registry = Registry::new();
//! let outcome = execute(&mut registry, Command::Add(String::from("codec"))).expect("valid");
//! assert!(outcome.changed());
//! assert_eq!(outcome.output(), "added 1: codec");
//! ```
//!
//! # Iterate through read-only views
//!
//! ```
//! use rust_foundations_lab_09_library_boundaries::Registry;
//!
//! let mut registry = Registry::new();
//! registry.add(String::from("one")).expect("valid");
//! registry.add(String::from("two")).expect("valid");
//! assert_eq!(registry.iter().map(|entry| entry.label).collect::<Vec<_>>(), vec!["one", "two"]);
//! ```
//!
//! # Privacy is a contract
//!
//! Registry fields are not a supported construction route.
//!
//! ```compile_fail,E0451
//! use rust_foundations_lab_09_library_boundaries::Registry;
//!
//! let registry = Registry { entries: Vec::new(), next_id: Some(1) };
//! # drop(registry);
//! ```

mod app;
mod command;
mod model;

pub use app::{AppError, Outcome, execute};
pub use command::{Command, CommandError, HELP, parse_command};
pub use model::{EntryId, EntryView, ParseEntryIdError, Registry, RegistryError};
