#![forbid(unsafe_code)]

//! CommandForge demonstrates a deliberately layered Rust metaprogramming system.
//!
//! Runtime command behavior is ordinary Rust. Declarative and procedural macros
//! own only mechanical relationships that would otherwise drift.
//!
//! ```
//! use commandforge::execute;
//! let args = ["run", "add", "--left", "20", "--right", "22"]
//!     .map(str::to_owned);
//! assert_eq!(execute(&args).unwrap().output, "42");
//! ```
//!
//! The argument derive rejects unsupported item shapes at compile time:
//!
//! ```compile_fail
//! use commandforge::CommandArgs;
//! #[derive(CommandArgs)]
//! enum NotACommand { A }
//! ```

extern crate self as commandforge;

mod app;
mod args;
mod catalog;
mod descriptor;
mod diagnostic;
mod error;
pub mod exit_codes;
pub mod handlers;

pub use app::{execute, exit_code_for_error, help_text, Execution};
pub use args::{ArgError, ArgumentSpec, CommandArgs};
pub use catalog::{find_command, COMMANDS};
pub use descriptor::{CommandSpec, HandlerDescriptor};
pub use diagnostic::Diagnostic;
pub use error::{AppError, CommandError};
pub use commandforge_macros::{command_catalog, command_handler, CommandArgs};
