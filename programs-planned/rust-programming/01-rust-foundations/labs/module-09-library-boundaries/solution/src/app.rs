//! Application orchestration for parsed registry commands.

use crate::{Command, HELP, Registry, RegistryError};
use std::error::Error;
use std::fmt;

/// The observable result of executing one command.
///
/// `changed` lets the process boundary decide whether persistent state must be
/// rewritten without teaching that boundary how each domain command behaves.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Outcome {
    output: String,
    changed: bool,
}

impl Outcome {
    /// Returns the text intended for standard output.
    pub fn output(&self) -> &str {
        &self.output
    }

    /// Reports whether successful execution changed registry state.
    pub const fn changed(&self) -> bool {
        self.changed
    }
}

/// A domain failure observed through the application boundary.
#[derive(Debug)]
pub struct AppError(RegistryError);

impl fmt::Display for AppError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

impl Error for AppError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        Some(&self.0)
    }
}

impl From<RegistryError> for AppError {
    fn from(error: RegistryError) -> Self {
        Self(error)
    }
}

/// Executes one typed command against a registry.
///
/// Parsing is intentionally absent from this function. Callers that already
/// hold a typed command do not need to reconstruct command-line text.
pub fn execute(registry: &mut Registry, command: Command) -> Result<Outcome, AppError> {
    match command {
        Command::Add(label) => {
            let id = registry.add(label)?;
            let entry = registry.get(id).ok_or(RegistryError::NotFound(id))?;
            Ok(Outcome {
                output: format!("added {id}: {}", entry.label),
                changed: true,
            })
        }
        Command::Remove(id) => {
            let label = registry.remove(id)?;
            Ok(Outcome {
                output: format!("removed {id}: {label}"),
                changed: true,
            })
        }
        Command::Find(id) => {
            let entry = registry.get(id).ok_or(RegistryError::NotFound(id))?;
            Ok(Outcome {
                output: format!("{}: {}", entry.id, entry.label),
                changed: false,
            })
        }
        Command::List => {
            let rows: Vec<_> = registry
                .iter()
                .map(|entry| format!("{}: {}", entry.id, entry.label))
                .collect();
            let output = if rows.is_empty() {
                String::from("no entries")
            } else {
                rows.join("\n")
            };
            Ok(Outcome {
                output,
                changed: false,
            })
        }
        Command::Help => Ok(Outcome {
            output: HELP.to_owned(),
            changed: false,
        }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn read_only_commands_do_not_claim_mutation() {
        let mut registry = Registry::new();
        assert!(
            !execute(&mut registry, Command::List)
                .expect("list is valid")
                .changed()
        );
        assert!(
            !execute(&mut registry, Command::Help)
                .expect("help is valid")
                .changed()
        );
    }
}
