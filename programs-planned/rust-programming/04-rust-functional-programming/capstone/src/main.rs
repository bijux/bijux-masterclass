#![forbid(unsafe_code)]

use ledgerflow::app::{AppOutcome, Command, execute_text, parse_args};
use std::env;
use std::fs;
use std::io::{self, Write};
use std::process::ExitCode;

fn main() -> ExitCode {
    let outcome = match parse_args(env::args().skip(1)) {
        Ok(command) => execute(command),
        Err(error) => AppOutcome::failure(error.message()),
    };

    if !outcome.stdout().is_empty()
        && writeln!(io::stdout(), "{}", outcome.stdout()).is_err()
    {
        return ExitCode::from(2);
    }
    if !outcome.stderr().is_empty()
        && writeln!(io::stderr(), "{}", outcome.stderr()).is_err()
    {
        return ExitCode::from(2);
    }
    ExitCode::from(outcome.exit_code())
}

fn execute(command: Command) -> AppOutcome {
    let Some(path) = command.path() else {
        return execute_text(&command, "");
    };
    match fs::read_to_string(path) {
        Ok(input) => execute_text(&command, &input),
        Err(error) => AppOutcome::failure(format!("cannot read {}: {error}", path.display())),
    }
}
