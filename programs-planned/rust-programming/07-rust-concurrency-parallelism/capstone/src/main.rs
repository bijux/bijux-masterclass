use batchweave::run_arguments;
use std::io::{self, Write};

fn main() {
    let arguments = std::env::args_os().skip(1);
    match run_arguments(arguments) {
        Ok(output) => {
            if !output.stdout.is_empty() {
                print_best_effort(&mut io::stdout().lock(), &output.stdout);
            }
            if !output.stderr.is_empty() {
                print_best_effort(&mut io::stderr().lock(), &output.stderr);
            }
            std::process::exit(output.exit_code);
        }
        Err(error) => {
            print_best_effort(&mut io::stderr().lock(), &format!("batchweave: {error}\n"));
            std::process::exit(2);
        }
    }
}

fn print_best_effort(writer: &mut impl Write, value: &str) {
    let _ = writer.write_all(value.as_bytes());
    let _ = writer.flush();
}
