//! Command-line text parsing into a typed command model.

use crate::EntryId;
use std::error::Error;
use std::fmt;

/// Stable command reference shown by the process boundary.
pub const HELP: &str =
    "registry commands:\n  add <label...>\n  remove <id>\n  find <id>\n  list\n  help";

/// A command whose syntax and argument types have already been validated.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    /// Insert an entry with the supplied owned label.
    Add(String),
    /// Remove the identified entry.
    Remove(EntryId),
    /// Read one identified entry.
    Find(EntryId),
    /// List every entry in deterministic insertion order.
    List,
    /// Render the stable command reference.
    Help,
}

/// A failure while converting argument text into a [`Command`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CommandError {
    /// No command name was supplied.
    MissingCommand,
    /// The command name is not part of the grammar.
    UnknownCommand(String),
    /// A required operand was omitted.
    MissingArgument(&'static str),
    /// A command received more operands than its grammar permits.
    UnexpectedArguments(&'static str),
    /// An entry ID was not a positive integer.
    InvalidId(String),
}

impl fmt::Display for CommandError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingCommand => write!(formatter, "missing command"),
            Self::UnknownCommand(command) => {
                write!(formatter, "unknown command `{command}`")
            }
            Self::MissingArgument(argument) => write!(formatter, "missing {argument}"),
            Self::UnexpectedArguments(command) => {
                write!(formatter, "{command} does not accept arguments")
            }
            Self::InvalidId(value) => {
                write!(formatter, "invalid nonzero entry ID `{value}`")
            }
        }
    }
}

impl Error for CommandError {}

/// Parses arguments after the executable name into one typed command.
pub fn parse_command(args: &[String]) -> Result<Command, CommandError> {
    let Some((command, rest)) = args.split_first() else {
        return Err(CommandError::MissingCommand);
    };

    match command.as_str() {
        "add" => {
            if rest.is_empty() {
                return Err(CommandError::MissingArgument("label"));
            }
            Ok(Command::Add(rest.join(" ")))
        }
        "remove" => Ok(Command::Remove(parse_single_id(rest, "remove")?)),
        "find" => Ok(Command::Find(parse_single_id(rest, "find")?)),
        "list" => {
            require_empty(rest, "list")?;
            Ok(Command::List)
        }
        "help" | "--help" | "-h" => {
            require_empty(rest, "help")?;
            Ok(Command::Help)
        }
        other => Err(CommandError::UnknownCommand(other.to_owned())),
    }
}

fn parse_single_id(
    args: &[String],
    command: &'static str,
) -> Result<EntryId, CommandError> {
    match args {
        [] => Err(CommandError::MissingArgument("entry ID")),
        [value] => value
            .parse::<EntryId>()
            .map_err(|_| CommandError::InvalidId(value.clone())),
        _ => Err(CommandError::UnexpectedArguments(command)),
    }
}

fn require_empty(args: &[String], command: &'static str) -> Result<(), CommandError> {
    if args.is_empty() {
        Ok(())
    } else {
        Err(CommandError::UnexpectedArguments(command))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn args(values: &[&str]) -> Vec<String> {
        values.iter().map(|value| (*value).to_owned()).collect()
    }

    #[test]
    fn parser_joins_owned_label() {
        assert_eq!(
            parse_command(&args(&["add", "record", "parser"])),
            Ok(Command::Add(String::from("record parser")))
        );
    }

    #[test]
    fn parser_rejects_ambiguous_arity() {
        assert_eq!(
            parse_command(&args(&["remove", "1", "2"])),
            Err(CommandError::UnexpectedArguments("remove"))
        );
        assert_eq!(
            parse_command(&args(&["list", "extra"])),
            Err(CommandError::UnexpectedArguments("list"))
        );
    }
}
