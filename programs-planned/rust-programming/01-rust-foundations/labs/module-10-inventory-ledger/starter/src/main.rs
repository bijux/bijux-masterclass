use rust_foundations_lab_10_inventory_ledger_starter::help;
use std::env;
use std::process::ExitCode;

fn main() -> ExitCode {
    let args = env::args().skip(1).collect::<Vec<_>>();
    let requests_help = args.is_empty()
        || (args.len() == 1 && matches!(args[0].as_str(), "help" | "--help"));
    if requests_help {
        print!("{}", help());
        ExitCode::SUCCESS
    } else {
        eprintln!("the starter implements only help; build the contract in ../README.md");
        ExitCode::from(2)
    }
}
