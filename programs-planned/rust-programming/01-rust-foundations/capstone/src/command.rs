use crate::{
    ParsePriorityError, ParseStatusError, ParseTaskIdError, Priority, Status, TaskId,
};
use std::error::Error;
use std::fmt;

/// Complete command-line grammar after successful parsing.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    /// Add a new `todo` task.
    Add {
        /// Scheduling importance.
        priority: Priority,
        /// Owned title assembled from remaining command-line tokens.
        title: String,
    },
    /// List every task or only one lifecycle state.
    List {
        /// Optional status filter.
        status: Option<Status>,
    },
    /// Move a `todo` task to `doing`.
    Start(TaskId),
    /// Move a `doing` task to `done`.
    Done(TaskId),
    /// Move a `done` task back to `todo`.
    Reopen(TaskId),
    /// Remove a task permanently.
    Remove(TaskId),
    /// Replace a task title after validating the same storage invariant used by `add`.
    Rename {
        /// Task to modify.
        id: TaskId,
        /// New owned title assembled from the remaining command-line tokens.
        title: String,
    },
    /// Search titles using ASCII case-insensitive matching.
    Search(String),
    /// Print state counts.
    Stats,
    /// Print command documentation.
    Help,
    /// Print the package version.
    Version,
}

/// Stable command reference printed by `taskboard help`.
pub const HELP: &str = "taskboard — persistent local work queue\n\
\n\
USAGE:\n\
  taskboard add <low|normal|high> <title...>\n\
  taskboard list [todo|doing|done]\n\
  taskboard start <id>\n\
  taskboard done <id>\n\
  taskboard reopen <id>\n\
  taskboard remove <id>\n\
  taskboard rename <id> <title...>\n\
  taskboard search <query...>\n\
  taskboard stats\n\
  taskboard help\n\
  taskboard version\n\
\n\
ENVIRONMENT:\n\
  TASKBOARD_FILE   storage path; defaults to .taskboard.db\n";

/// Failure to convert raw argument tokens into one typed [`Command`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CommandParseError {
    /// No command token was supplied.
    MissingCommand,
    /// The first token did not name a supported command.
    UnknownCommand(String),
    /// A command did not receive all required operands.
    MissingArgument {
        /// Command whose grammar was incomplete.
        command: &'static str,
        /// Canonical usage form.
        usage: &'static str,
    },
    /// A command received more operands than its grammar permits.
    UnexpectedArgument {
        /// Command whose grammar was exceeded.
        command: &'static str,
        /// Canonical usage form.
        usage: &'static str,
    },
    /// A task ID token was invalid.
    InvalidId(ParseTaskIdError),
    /// A priority token was invalid.
    InvalidPriority(ParsePriorityError),
    /// A status token was invalid.
    InvalidStatus(ParseStatusError),
    /// The assembled title was blank.
    EmptyTitle,
    /// The assembled search query was blank.
    EmptyQuery,
}

impl fmt::Display for CommandParseError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingCommand => formatter.write_str("missing command; run `taskboard help`"),
            Self::UnknownCommand(command) => {
                write!(formatter, "unknown command `{command}`; run `taskboard help`")
            }
            Self::MissingArgument { command, usage } => {
                write!(formatter, "missing argument for `{command}`; usage: {usage}")
            }
            Self::UnexpectedArgument { command, usage } => {
                write!(formatter, "unexpected argument for `{command}`; usage: {usage}")
            }
            Self::InvalidId(error) => error.fmt(formatter),
            Self::InvalidPriority(error) => error.fmt(formatter),
            Self::InvalidStatus(error) => error.fmt(formatter),
            Self::EmptyTitle => formatter.write_str("task title cannot be empty"),
            Self::EmptyQuery => formatter.write_str("search query cannot be empty"),
        }
    }
}

impl Error for CommandParseError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::InvalidId(error) => Some(error),
            Self::InvalidPriority(error) => Some(error),
            Self::InvalidStatus(error) => Some(error),
            _ => None,
        }
    }
}

/// Parses command-line tokens that exclude the executable name.
pub fn parse_command(arguments: &[String]) -> Result<Command, CommandParseError> {
    let (name, operands) = arguments
        .split_first()
        .ok_or(CommandParseError::MissingCommand)?;

    match name.as_str() {
        "add" => parse_add(operands),
        "list" => parse_list(operands),
        "start" => parse_id_command(operands, "start", "taskboard start <id>", Command::Start),
        "done" => parse_id_command(operands, "done", "taskboard done <id>", Command::Done),
        "reopen" => parse_id_command(
            operands,
            "reopen",
            "taskboard reopen <id>",
            Command::Reopen,
        ),
        "remove" => parse_id_command(
            operands,
            "remove",
            "taskboard remove <id>",
            Command::Remove,
        ),
        "rename" => parse_rename(operands),
        "search" => parse_search(operands),
        "stats" => parse_zero_operand(operands, "stats", "taskboard stats", Command::Stats),
        "help" | "--help" | "-h" => {
            parse_zero_operand(operands, "help", "taskboard help", Command::Help)
        }
        "version" | "--version" | "-V" => parse_zero_operand(
            operands,
            "version",
            "taskboard version",
            Command::Version,
        ),
        unknown => Err(CommandParseError::UnknownCommand(unknown.to_owned())),
    }
}

fn parse_add(operands: &[String]) -> Result<Command, CommandParseError> {
    let (priority, title_tokens) = operands
        .split_first()
        .ok_or(CommandParseError::MissingArgument {
            command: "add",
            usage: "taskboard add <low|normal|high> <title...>",
        })?;

    if title_tokens.is_empty() {
        return Err(CommandParseError::MissingArgument {
            command: "add",
            usage: "taskboard add <low|normal|high> <title...>",
        });
    }

    let priority = priority
        .parse::<Priority>()
        .map_err(CommandParseError::InvalidPriority)?;
    let title = title_tokens.join(" ");
    if title.trim().is_empty() {
        return Err(CommandParseError::EmptyTitle);
    }
    Ok(Command::Add { priority, title })
}

fn parse_list(operands: &[String]) -> Result<Command, CommandParseError> {
    match operands {
        [] => Ok(Command::List { status: None }),
        [status] => status
            .parse::<Status>()
            .map(|status| Command::List {
                status: Some(status),
            })
            .map_err(CommandParseError::InvalidStatus),
        _ => Err(CommandParseError::UnexpectedArgument {
            command: "list",
            usage: "taskboard list [todo|doing|done]",
        }),
    }
}

fn parse_id_command(
    operands: &[String],
    command: &'static str,
    usage: &'static str,
    constructor: fn(TaskId) -> Command,
) -> Result<Command, CommandParseError> {
    match operands {
        [] => Err(CommandParseError::MissingArgument { command, usage }),
        [id] => id
            .parse::<TaskId>()
            .map(constructor)
            .map_err(CommandParseError::InvalidId),
        _ => Err(CommandParseError::UnexpectedArgument { command, usage }),
    }
}

fn parse_rename(operands: &[String]) -> Result<Command, CommandParseError> {
    let (id, title_tokens) = operands
        .split_first()
        .ok_or(CommandParseError::MissingArgument {
            command: "rename",
            usage: "taskboard rename <id> <title...>",
        })?;

    if title_tokens.is_empty() {
        return Err(CommandParseError::MissingArgument {
            command: "rename",
            usage: "taskboard rename <id> <title...>",
        });
    }

    let id = id
        .parse::<TaskId>()
        .map_err(CommandParseError::InvalidId)?;
    let title = title_tokens.join(" ");
    if title.trim().is_empty() {
        return Err(CommandParseError::EmptyTitle);
    }
    Ok(Command::Rename { id, title })
}

fn parse_search(operands: &[String]) -> Result<Command, CommandParseError> {
    if operands.is_empty() {
        return Err(CommandParseError::MissingArgument {
            command: "search",
            usage: "taskboard search <query...>",
        });
    }
    let query = operands.join(" ");
    if query.trim().is_empty() {
        return Err(CommandParseError::EmptyQuery);
    }
    Ok(Command::Search(query))
}

fn parse_zero_operand(
    operands: &[String],
    command: &'static str,
    usage: &'static str,
    parsed: Command,
) -> Result<Command, CommandParseError> {
    if operands.is_empty() {
        Ok(parsed)
    } else {
        Err(CommandParseError::UnexpectedArgument { command, usage })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn strings(values: &[&str]) -> Vec<String> {
        values.iter().map(|value| (*value).to_owned()).collect()
    }

    #[test]
    fn add_owns_a_joined_title() {
        assert_eq!(
            parse_command(&strings(&["add", "high", "Repair", "the", "codec"])),
            Ok(Command::Add {
                priority: Priority::High,
                title: String::from("Repair the codec"),
            })
        );
    }

    #[test]
    fn list_accepts_zero_or_one_status() {
        assert_eq!(
            parse_command(&strings(&["list"])),
            Ok(Command::List { status: None })
        );
        assert_eq!(
            parse_command(&strings(&["list", "done"])),
            Ok(Command::List {
                status: Some(Status::Done),
            })
        );
        assert!(matches!(
            parse_command(&strings(&["list", "done", "extra"])),
            Err(CommandParseError::UnexpectedArgument { .. })
        ));
    }

    #[test]
    fn id_commands_are_strict_about_arity_and_nonzero_ids() {
        assert!(matches!(
            parse_command(&strings(&["start"])),
            Err(CommandParseError::MissingArgument { .. })
        ));
        assert!(matches!(
            parse_command(&strings(&["start", "0"])),
            Err(CommandParseError::InvalidId(_))
        ));
        assert!(matches!(
            parse_command(&strings(&["start", "1", "2"])),
            Err(CommandParseError::UnexpectedArgument { .. })
        ));
    }

    #[test]
    fn rename_requires_an_id_and_owns_the_remaining_title() {
        assert_eq!(
            parse_command(&strings(&["rename", "7", "Rebuild", "storage", "proof"])),
            Ok(Command::Rename {
                id: TaskId::new(7).expect("test ID is nonzero"),
                title: String::from("Rebuild storage proof"),
            })
        );
        assert!(matches!(
            parse_command(&strings(&["rename", "7"])),
            Err(CommandParseError::MissingArgument { .. })
        ));
        assert!(matches!(
            parse_command(&strings(&["rename", "zero", "Title"])),
            Err(CommandParseError::InvalidId(_))
        ));
    }

    #[test]
    fn aliases_do_not_accept_extra_operands() {
        assert_eq!(parse_command(&strings(&["--help"])), Ok(Command::Help));
        assert_eq!(
            parse_command(&strings(&["--version"])),
            Ok(Command::Version)
        );
        assert!(parse_command(&strings(&["-h", "extra"])).is_err());
    }

    #[test]
    fn missing_and_unknown_commands_are_distinct() {
        assert_eq!(
            parse_command(&[]),
            Err(CommandParseError::MissingCommand)
        );
        assert_eq!(
            parse_command(&strings(&["launch"])),
            Err(CommandParseError::UnknownCommand(String::from("launch")))
        );
    }
}
