
use framevault::app;
use std::ffi::OsString;
use std::io::{self, Write};
use std::process::ExitCode;

fn emit_test(mut arguments: impl Iterator<Item = OsString>) -> ExitCode {
    let stdout = arguments
        .next()
        .and_then(|value| value.into_string().ok())
        .unwrap_or_default();
    let stderr = arguments
        .next()
        .and_then(|value| value.into_string().ok())
        .unwrap_or_default();
    let code = arguments
        .next()
        .and_then(|value| value.into_string().ok())
        .and_then(|value| value.parse::<u8>().ok())
        .unwrap_or(0);
    let _ = io::stdout().write_all(stdout.as_bytes());
    let _ = io::stderr().write_all(stderr.as_bytes());
    ExitCode::from(code)
}

fn main() -> ExitCode {
    let mut arguments = std::env::args_os().skip(1);
    if arguments
        .next()
        .is_some_and(|value| value == OsString::from("__emit-test"))
    {
        return emit_test(arguments);
    }

    match app::run(std::env::args_os().skip(1)) {
        Ok(result) => {
            if let Err(error) = io::stdout().write_all(result.stdout.as_bytes()) {
                let _ = writeln!(io::stderr(), "framevault: could not write stdout: {error}");
                return ExitCode::from(1);
            }
            ExitCode::from(u8::try_from(result.exit_code).unwrap_or(1))
        }
        Err(error) => {
            let _ = writeln!(io::stderr(), "framevault: {error}");
            ExitCode::from(u8::try_from(error.exit_code()).unwrap_or(1))
        }
    }
}
