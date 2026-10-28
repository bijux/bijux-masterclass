//! Persistent task board used as the cumulative Rust Foundations capstone.
//!
//! The crate separates domain rules, command parsing, storage, and application
//! coordination so each contract can be tested at its proper boundary.
//!
//! # Domain use
//!
//! ```
//! use taskboard::{Priority, Status, TaskBoard};
//!
//! let mut board = TaskBoard::new();
//! let id = board
//!     .add(Priority::High, String::from("Repair parser"))
//!     .expect("valid title and available ID");
//! board.start(id).expect("new tasks may be started");
//!
//! let task = board.find(id).expect("task exists");
//! assert_eq!(task.status(), Status::Doing);
//! ```
//!
//! # Typed command parsing
//!
//! ```
//! use taskboard::{Command, Priority, parse_command};
//!
//! let arguments = vec![
//!     String::from("add"),
//!     String::from("high"),
//!     String::from("Repair"),
//!     String::from("codec"),
//! ];
//!
//! assert!(matches!(
//!     parse_command(&arguments),
//!     Ok(Command::Add { priority: Priority::High, title }) if title == "Repair codec"
//! ));
//! ```
//!
//! # Generic in-memory persistence
//!
//! ```
//! use std::io::Cursor;
//! use taskboard::{Priority, TaskBoard, load_from, save_to};
//!
//! let mut board = TaskBoard::new();
//! board
//!     .add(Priority::Normal, String::from("Write tests"))
//!     .expect("valid task");
//!
//! let mut bytes = Vec::new();
//! save_to(&mut bytes, &board).expect("memory writer");
//! let restored = load_from(Cursor::new(bytes)).expect("memory reader");
//! assert_eq!(restored.tasks().len(), 1);
//! ```

mod app;
mod command;
mod model;
mod storage;

pub use app::{Outcome, RunError, execute, run};
pub use command::{Command, CommandParseError, HELP, parse_command};
pub use model::{
    ParsePriorityError, ParseStatusError, ParseTaskIdError, Priority, Stats, Status, Task,
    TaskBoard, TaskError, TaskId,
};
pub use storage::{RecordError, StorageError, load_from, load_path, save_path, save_to};
