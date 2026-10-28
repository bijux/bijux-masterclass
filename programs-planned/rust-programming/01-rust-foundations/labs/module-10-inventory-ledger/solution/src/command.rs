use crate::ItemId;
use std::error::Error;
use std::fmt;

/// Stable command help.
pub const HELP: &str = concat!(
    "inventory-ledger commands:\n",
    "  add <name...>\n",
    "  checkout <id> <borrower...>\n",
    "  return <id>\n",
    "  retire <id>\n",
    "  list [available|checked-out|retired]\n",
    "  search <query...>\n",
    "  stats\n",
    "  help",
);

/// Optional list filter independent of borrower payload.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Filter {
    /// Available items.
    Available,
    /// Checked-out items.
    CheckedOut,
    /// Retired items.
    Retired,
}

/// Typed inventory command.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    /// Add an owned item name.
    Add(String),
    /// Check out one item to an owned borrower.
    Checkout {
        /// Target item.
        id: ItemId,
        /// Borrower to store in state.
        borrower: String,
    },
    /// Return one item.
    Return(ItemId),
    /// Retire one item.
    Retire(ItemId),
    /// List all or one state.
    List(Option<Filter>),
    /// Search names.
    Search(String),
    /// Render counts.
    Stats,
    /// Render help without loading storage.
    Help,
}

/// Failure while converting arguments to a typed command.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CommandError {
    /// No command was supplied.
    MissingCommand,
    /// Command name was unknown.
    UnknownCommand(String),
    /// Required argument was absent.
    MissingArgument(&'static str),
    /// Fixed-arity command received extra text.
    UnexpectedArguments(&'static str),
    /// ID text was invalid.
    InvalidId(String),
    /// List filter was unknown.
    InvalidFilter(String),
}

impl fmt::Display for CommandError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingCommand => write!(formatter, "missing command"),
            Self::UnknownCommand(value) => write!(formatter, "unknown command `{value}`"),
            Self::MissingArgument(value) => write!(formatter, "missing {value}"),
            Self::UnexpectedArguments(value) => {
                write!(formatter, "{value} received unexpected arguments")
            }
            Self::InvalidId(value) => write!(formatter, "invalid nonzero item ID `{value}`"),
            Self::InvalidFilter(value) => write!(formatter, "invalid list filter `{value}`"),
        }
    }
}

impl Error for CommandError {}

/// Parses process arguments excluding executable name.
pub fn parse_command(args: &[String]) -> Result<Command, CommandError> {
    let Some((name, rest)) = args.split_first() else {
        return Err(CommandError::MissingCommand);
    };
    match name.as_str() {
        "add" => Ok(Command::Add(join_required(rest, "item name")?)),
        "checkout" => {
            let Some((id, borrower)) = rest.split_first() else {
                return Err(CommandError::MissingArgument("item ID"));
            };
            let id = parse_id(id)?;
            Ok(Command::Checkout { id, borrower: join_required(borrower, "borrower")? })
        }
        "return" => Ok(Command::Return(single_id(rest, "return")?)),
        "retire" => Ok(Command::Retire(single_id(rest, "retire")?)),
        "list" => match rest {
            [] => Ok(Command::List(None)),
            [filter] => Ok(Command::List(Some(parse_filter(filter)?))),
            _ => Err(CommandError::UnexpectedArguments("list")),
        },
        "search" => Ok(Command::Search(join_required(rest, "search query")?)),
        "stats" => {
            require_empty(rest, "stats")?;
            Ok(Command::Stats)
        }
        "help" | "-h" | "--help" => {
            require_empty(rest, "help")?;
            Ok(Command::Help)
        }
        other => Err(CommandError::UnknownCommand(other.to_owned())),
    }
}

fn join_required(values: &[String], name: &'static str) -> Result<String, CommandError> {
    if values.is_empty() {
        Err(CommandError::MissingArgument(name))
    } else {
        Ok(values.join(" "))
    }
}

fn parse_id(value: &str) -> Result<ItemId, CommandError> {
    value.parse::<ItemId>().map_err(|_| CommandError::InvalidId(value.to_owned()))
}

fn single_id(values: &[String], command: &'static str) -> Result<ItemId, CommandError> {
    match values {
        [] => Err(CommandError::MissingArgument("item ID")),
        [value] => parse_id(value),
        _ => Err(CommandError::UnexpectedArguments(command)),
    }
}

fn parse_filter(value: &str) -> Result<Filter, CommandError> {
    match value {
        "available" => Ok(Filter::Available),
        "checked-out" => Ok(Filter::CheckedOut),
        "retired" => Ok(Filter::Retired),
        other => Err(CommandError::InvalidFilter(other.to_owned())),
    }
}

fn require_empty(values: &[String], command: &'static str) -> Result<(), CommandError> {
    if values.is_empty() {
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
    fn checkout_separates_id_from_multiword_borrower() {
        assert!(matches!(
            parse_command(&args(&["checkout", "2", "Grace", "Hopper"])),
            Ok(Command::Checkout { id, borrower }) if id.get() == 2 && borrower == "Grace Hopper"
        ));
    }

    #[test]
    fn fixed_arity_commands_reject_extra_data() {
        assert_eq!(
            parse_command(&args(&["return", "1", "extra"])),
            Err(CommandError::UnexpectedArguments("return"))
        );
        assert_eq!(
            parse_command(&args(&["stats", "extra"])),
            Err(CommandError::UnexpectedArguments("stats"))
        );
    }
}
