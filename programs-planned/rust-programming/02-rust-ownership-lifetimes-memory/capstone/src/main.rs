use memory_workspace::ScriptEngine;
use std::env;
use std::fs;
use std::process::ExitCode;
const DEMO: &str = "ADD\tdoc\tMemory contracts\tOwnership makes cleanup explicit.\n\
SHOW\tdoc\n\
SNAPSHOT\tsnap0\tdoc\n\
WATCH\twatch0\tsnap0\n\
EDIT\tdoc\t0\tOwnership, lifetimes, and memory make cleanup explicit.\n\
SEARCH\tcleanup\n\
MEMORY\n\
EVICT\tdoc\t0\n\
DROP-SNAPSHOT\tsnap0\n\
CHECK-WATCH\twatch0\n\
SHOW\tdoc\n";
fn main() -> ExitCode {
    match run(env::args().skip(1).collect()) {
        Ok(lines) => {
            for line in lines {
                println!("{line}");
            }
            ExitCode::SUCCESS
        }
        Err(error) => {
            eprintln!("error: {error}");
            ExitCode::FAILURE
        }
    }
}
fn run(arguments: Vec<String>) -> Result<Vec<String>, String> {
    let mut engine = ScriptEngine::new();
    match arguments.as_slice() {
        [command] if command == "demo" => {
            engine.execute(DEMO).map_err(|error| error.to_string())
        }
        [command, path] if command == "script" => {
            let source = fs::read_to_string(path)
            .map_err(|error| format!("cannot read {path}: {error}"))?;
            engine.execute(&source).map_err(|error| error.to_string())
        }
        [command] if command == "help" => Ok(vec![help_text().to_owned()]),
        [command] if command == "version" => Ok(vec![format!(
        "memory-workspace {}",
        env!("CARGO_PKG_VERSION")
        )]),
        [] => Ok(vec![help_text().to_owned()]),
        _ => Err(String::from(
        "usage: memory-workspace demo | script <path> | help | version",
        )),
    }
}
fn help_text() -> &'static str {
    concat!(
        "memory-workspace\n\n",
        "  demo           run the deterministic ownership-topology scenario\n",
        "  script <path>  execute a tab-separated workspace script\n",
        "  help           show this text\n",
        "  version        show the package version\n\n",
        "See capstone/README.md for the script grammar.",
    )
}
