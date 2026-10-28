use rust_foundations_lab_09_library_boundaries::{Registry, execute, parse_command};
use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let command = match parse_command(&args) {
        Ok(command) => command,
        Err(error) => {
            eprintln!("error: {error}");
            return ExitCode::from(2);
        }
    };
    let mut registry = Registry::new();
    match execute(&mut registry, command) {
        Ok(outcome) => {
            println!("{}", outcome.output());
            ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("error: {error}");
            ExitCode::from(1)
        }
    }
}
