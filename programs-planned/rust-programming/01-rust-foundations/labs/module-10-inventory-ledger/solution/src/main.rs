use rust_foundations_lab_10_inventory_ledger::{RunError, run};
use std::path::PathBuf;
use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let path = std::env::var_os("INVENTORY_LEDGER_FILE")
        .map_or_else(|| PathBuf::from(".inventory-ledger.db"), PathBuf::from);
    match run(&args, &path) {
        Ok(output) => {
            println!("{output}");
            ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("error: {error}");
            match error {
                RunError::Command(_) => ExitCode::from(2),
                RunError::Storage(_) | RunError::Domain(_) => ExitCode::from(1),
            }
        }
    }
}
