use crate::{
    Command, CommandError, DomainError, Filter, HELP, Item, ItemState, Ledger, StorageError,
    load_path, parse_command, save_path,
};
use std::error::Error;
use std::fmt;
use std::path::Path;

/// User-visible output and mutation fact for one command.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Outcome {
    output: String,
    changed: bool,
}

impl Outcome {
    /// Borrows deterministic output.
    pub fn output(&self) -> &str {
        &self.output
    }

    /// Reports whether persistence is required.
    pub const fn changed(&self) -> bool {
        self.changed
    }
}

/// End-to-end command failure.
#[derive(Debug)]
pub enum RunError {
    /// Arguments could not be typed.
    Command(CommandError),
    /// Snapshot could not be loaded or saved.
    Storage(StorageError),
    /// Domain invariant or transition failed.
    Domain(DomainError),
}

impl fmt::Display for RunError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Command(error) => error.fmt(formatter),
            Self::Storage(error) => error.fmt(formatter),
            Self::Domain(error) => error.fmt(formatter),
        }
    }
}

impl Error for RunError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Command(error) => Some(error),
            Self::Storage(error) => Some(error),
            Self::Domain(error) => Some(error),
        }
    }
}

impl From<CommandError> for RunError {
    fn from(error: CommandError) -> Self {
        Self::Command(error)
    }
}
impl From<StorageError> for RunError {
    fn from(error: StorageError) -> Self {
        Self::Storage(error)
    }
}
impl From<DomainError> for RunError {
    fn from(error: DomainError) -> Self {
        Self::Domain(error)
    }
}

/// Applies a typed command without performing file I/O.
pub fn execute(ledger: &mut Ledger, command: Command) -> Result<Outcome, DomainError> {
    match command {
        Command::Add(name) => {
            let id = ledger.add(name)?;
            let item = ledger.find(id).ok_or(DomainError::NotFound(id))?;
            Ok(Outcome { output: format!("added {id}: {}", item.name()), changed: true })
        }
        Command::Checkout { id, borrower } => {
            ledger.checkout(id, borrower)?;
            Ok(Outcome { output: format!("checked out {id}"), changed: true })
        }
        Command::Return(id) => {
            ledger.return_item(id)?;
            Ok(Outcome { output: format!("returned {id}"), changed: true })
        }
        Command::Retire(id) => {
            ledger.retire(id)?;
            Ok(Outcome { output: format!("retired {id}"), changed: true })
        }
        Command::List(filter) => {
            let rows: Vec<_> = ledger
                .items()
                .iter()
                .filter(|item| filter.is_none_or(|filter| matches_filter(item, filter)))
                .map(render_item)
                .collect();
            Ok(Outcome {
                output: if rows.is_empty() {
                    String::from("no items")
                } else {
                    rows.join("\n")
                },
                changed: false,
            })
        }
        Command::Search(query) => {
            let rows: Vec<_> = ledger.search(&query).map(render_item).collect();
            Ok(Outcome {
                output: if rows.is_empty() {
                    String::from("no matches")
                } else {
                    rows.join("\n")
                },
                changed: false,
            })
        }
        Command::Stats => {
            let counts = ledger.counts();
            Ok(Outcome {
                output: format!(
                    "available: {}\nchecked-out: {}\nretired: {}\ntotal: {}",
                    counts.available,
                    counts.checked_out,
                    counts.retired,
                    counts.total()
                ),
                changed: false,
            })
        }
        Command::Help => Ok(Outcome { output: HELP.to_owned(), changed: false }),
    }
}

/// Parses, loads, executes, and saves one process invocation.
pub fn run(args: &[String], path: &Path) -> Result<String, RunError> {
    let command = parse_command(args)?;
    if command == Command::Help {
        return Ok(HELP.to_owned());
    }
    let mut ledger = load_path(path)?;
    let outcome = execute(&mut ledger, command)?;
    if outcome.changed {
        save_path(path, &ledger)?;
    }
    Ok(outcome.output)
}

fn matches_filter(item: &Item, filter: Filter) -> bool {
    matches!((item.state(), filter),
        (ItemState::Available, Filter::Available)
        | (ItemState::CheckedOut { .. }, Filter::CheckedOut)
        | (ItemState::Retired, Filter::Retired)
    )
}

fn render_item(item: &Item) -> String {
    match item.state() {
        ItemState::Available => format!("{} [available] {}", item.id(), item.name()),
        ItemState::CheckedOut { borrower } => {
            format!("{} [checked-out: {borrower}] {}", item.id(), item.name())
        }
        ItemState::Retired => format!("{} [retired] {}", item.id(), item.name()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn read_commands_do_not_request_save() {
        let mut ledger = Ledger::new();
        for command in [
            Command::List(None),
            Command::Search(String::from("x")),
            Command::Stats,
            Command::Help,
        ] {
            assert!(!execute(&mut ledger, command).expect("valid").changed());
        }
    }
}
