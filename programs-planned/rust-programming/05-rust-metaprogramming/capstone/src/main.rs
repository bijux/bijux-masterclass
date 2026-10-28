use commandforge::{execute, exit_code_for_error};

fn main() {
    let arguments = std::env::args().skip(1).collect::<Vec<_>>();
    match execute(&arguments) {
        Ok(execution) => {
            if !execution.output.is_empty() {
                println!("{}", execution.output);
            }
            std::process::exit(execution.exit_code);
        }
        Err(error) => {
            eprintln!("error: {error}");
            std::process::exit(exit_code_for_error(&error));
        }
    }
}
