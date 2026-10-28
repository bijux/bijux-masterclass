use std::env;
use std::io::{self, Write};
use std::path::PathBuf;
use std::process;
use taskboard::run;

fn main() {
    let arguments: Vec<String> = env::args().skip(1).collect();
    let storage_path = env::var_os("TASKBOARD_FILE")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from(".taskboard.db"));

    match run(&arguments, &storage_path) {
        Ok(output) => {
            if let Err(error) = io::stdout().lock().write_all(output.as_bytes()) {
                let _ignored = writeln!(
                    io::stderr().lock(),
                    "error: write standard output: {error}"
                );
                process::exit(1);
            }
        }
        Err(error) => {
            let _ignored = writeln!(io::stderr().lock(), "error: {error}");
            process::exit(error.exit_code());
        }
    }
}
