use std::{ffi::OsString, path::PathBuf};

use crate::{migrate_v0, LendingRecords, Record, Store, StoreError};

pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const SCHEMA: &str = "AXIOM01";

const MAX_RECORD: usize = 4096;
const TX_CAP: usize = 32;
type DefaultStore = Store<MAX_RECORD, TX_CAP>;

pub fn run<I>(arguments: I) -> Result<String, StoreError>
where
    I: IntoIterator<Item = OsString>,
{
    let mut args = arguments.into_iter();
    let _program = args.next();
    let Some(command) = args.next() else {
        return Ok(help());
    };
    let command = command.to_string_lossy();

    match command.as_ref() {
        "init" => {
            let path = required_path(args.next(), "init <archive.ax>")?;
            reject_extra(args)?;
            let snapshot = DefaultStore::new(&path)?.init()?;
            Ok(format!(
                "initialized {} with {} records\n",
                path.display(),
                snapshot.len()
            ))
        }
        "put" => {
            let path = required_path(args.next(), "put <archive.ax> <key> <value>")?;
            let key = required_text(args.next(), "put <archive.ax> <key> <value>")?;
            let value = required_text(args.next(), "put <archive.ax> <key> <value>")?;
            reject_extra(args)?;
            let snapshot = DefaultStore::new(&path)?.put(Record::new(key, value)?)?;
            Ok(format!("committed {} records\n", snapshot.len()))
        }
        "list" => {
            let path = required_path(args.next(), "list <archive.ax>")?;
            reject_extra(args)?;
            let snapshot = DefaultStore::new(path)?.open_snapshot()?;
            let mut cursor = snapshot.records();
            let mut output = String::new();
            while let Some(view) = cursor.next() {
                let view = view?;
                output.push_str(view.key());
                output.push('\t');
                output.push_str(view.value());
                output.push('\n');
            }
            Ok(output)
        }
        "verify" => {
            let path = required_path(args.next(), "verify <archive.ax>")?;
            reject_extra(args)?;
            let snapshot = DefaultStore::new(&path)?.open_snapshot()?;
            Ok(format!("ok\t{}\t{}\n", SCHEMA, snapshot.len()))
        }
        "migrate-v0" => {
            let source =
                required_path(args.next(), "migrate-v0 <legacy.txt> <archive.ax>")?;
            let destination =
                required_path(args.next(), "migrate-v0 <legacy.txt> <archive.ax>")?;
            reject_extra(args)?;
            let store = DefaultStore::new(&destination)?;
            let snapshot = migrate_v0(&source, &store)?;
            Ok(format!(
                "migrated {} records to {}\n",
                snapshot.len(),
                destination.display()
            ))
        }
        "schema" => {
            reject_extra(args)?;
            Ok(format!("{SCHEMA}\n"))
        }
        "version" | "--version" | "-V" => {
            reject_extra(args)?;
            Ok(format!("axiomstore {VERSION}\n"))
        }
        "help" | "--help" | "-h" => {
            reject_extra(args)?;
            Ok(help())
        }
        other => Err(StoreError::Usage(format!(
            "unknown command {other:?}\n\n{}",
            help()
        ))),
    }
}

pub fn help() -> String {
    "AxiomStore — versioned embedded records\n\n\
usage:\n\
  axiomstore init <archive.ax>\n\
  axiomstore put <archive.ax> <key> <value>\n\
  axiomstore list <archive.ax>\n\
  axiomstore verify <archive.ax>\n\
  axiomstore migrate-v0 <legacy.txt> <archive.ax>\n\
  axiomstore schema\n\
  axiomstore version\n\
  axiomstore help\n"
        .into()
}

fn required_path(value: Option<OsString>, usage: &str) -> Result<PathBuf, StoreError> {
    value
        .map(PathBuf::from)
        .ok_or_else(|| StoreError::Usage(format!("usage: axiomstore {usage}")))
}

fn required_text(value: Option<OsString>, usage: &str) -> Result<String, StoreError> {
    value
        .ok_or_else(|| StoreError::Usage(format!("usage: axiomstore {usage}")))?
        .into_string()
        .map_err(|_| StoreError::Usage("text arguments must be valid Unicode".into()))
}

fn reject_extra(mut args: impl Iterator<Item = OsString>) -> Result<(), StoreError> {
    if let Some(extra) = args.next() {
        Err(StoreError::Usage(format!(
            "unexpected argument {extra:?}"
        )))
    } else {
        Ok(())
    }
}
