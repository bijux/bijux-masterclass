//! Working but intentionally tangled registry CLI.
//!
//! Domain state, parsing, application behavior, rendering, and process handling
//! share this file so the laboratory can begin from characterized behavior.

use std::env;
use std::fmt;
use std::process::ExitCode;

const HELP: &str = "registry add <label...>\nregistry list\nregistry remove <id>\n";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct EntryId(u64);

impl EntryId {
    fn parse(raw: &str) -> Result<Self, String> {
        let value = raw
            .parse::<u64>()
            .map_err(|_| format!("invalid nonzero entry ID `{raw}`"))?;
        if value == 0 {
            return Err(format!("invalid nonzero entry ID `{raw}`"));
        }
        Ok(Self(value))
    }
}

impl fmt::Display for EntryId {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        self.0.fmt(formatter)
    }
}

#[derive(Debug, Default)]
struct Registry {
    entries: Vec<(EntryId, String)>,
    next_id: u64,
}

impl Registry {
    fn new() -> Self {
        Self {
            entries: Vec::new(),
            next_id: 1,
        }
    }

    fn add(&mut self, label: String) -> Result<EntryId, String> {
        let label = label.trim();
        if label.is_empty() {
            return Err(String::from("label cannot be empty"));
        }
        let id = EntryId(self.next_id);
        self.next_id = self
            .next_id
            .checked_add(1)
            .ok_or_else(|| String::from("entry ID space is exhausted"))?;
        self.entries.push((id, label.to_owned()));
        Ok(id)
    }

    fn remove(&mut self, id: EntryId) -> Result<String, String> {
        let index = self
            .entries
            .iter()
            .position(|(candidate, _)| *candidate == id)
            .ok_or_else(|| format!("entry {id} was not found"))?;
        Ok(self.entries.remove(index).1)
    }

    fn render(&self) -> String {
        if self.entries.is_empty() {
            return String::from("no entries");
        }
        self.entries
            .iter()
            .map(|(id, label)| format!("{id}\t{label}"))
            .collect::<Vec<_>>()
            .join("\n")
    }
}

fn parse_and_execute(registry: &mut Registry, args: &[String]) -> Result<String, String> {
    let Some(command) = args.first().map(String::as_str) else {
        return Ok(HELP.trim_end().to_owned());
    };
    match command {
        "add" => {
            if args.len() < 2 {
                return Err(String::from("usage: registry add <label...>"));
            }
            let id = registry.add(args[1..].join(" "))?;
            Ok(format!("added {id}"))
        }
        "list" if args.len() == 1 => Ok(registry.render()),
        "remove" if args.len() == 2 => {
            let id = EntryId::parse(&args[1])?;
            let label = registry.remove(id)?;
            Ok(format!("removed {id}\t{label}"))
        }
        "help" if args.len() == 1 => Ok(HELP.trim_end().to_owned()),
        "list" => Err(String::from("usage: registry list")),
        "remove" => Err(String::from("usage: registry remove <id>")),
        other => Err(format!("unknown command `{other}`")),
    }
}

fn main() -> ExitCode {
    let args = env::args().skip(1).collect::<Vec<_>>();
    let mut registry = Registry::new();
    match parse_and_execute(&mut registry, &args) {
        Ok(output) => {
            println!("{output}");
            ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("error: {error}");
            ExitCode::from(2)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn strings(values: &[&str]) -> Vec<String> {
        values.iter().map(|value| (*value).to_owned()).collect()
    }

    #[test]
    fn characterized_add_list_remove_flow() {
        let mut registry = Registry::new();
        assert_eq!(
            parse_and_execute(&mut registry, &strings(&["add", "Rust", "Book"])),
            Ok(String::from("added 1"))
        );
        assert_eq!(
            parse_and_execute(&mut registry, &strings(&["list"])),
            Ok(String::from("1\tRust Book"))
        );
        assert_eq!(
            parse_and_execute(&mut registry, &strings(&["remove", "1"])),
            Ok(String::from("removed 1\tRust Book"))
        );
        assert_eq!(registry.render(), "no entries");
    }

    #[test]
    fn characterized_errors_are_stable() {
        let mut registry = Registry::new();
        assert_eq!(
            parse_and_execute(&mut registry, &strings(&["add", "   "])),
            Err(String::from("label cannot be empty"))
        );
        assert_eq!(
            parse_and_execute(&mut registry, &strings(&["remove", "0"])),
            Err(String::from("invalid nonzero entry ID `0`"))
        );
        assert_eq!(
            parse_and_execute(&mut registry, &strings(&["unknown"])),
            Err(String::from("unknown command `unknown`"))
        );
    }
}
