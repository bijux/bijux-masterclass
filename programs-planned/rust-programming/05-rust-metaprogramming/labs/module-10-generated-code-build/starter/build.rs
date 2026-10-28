use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    println!("cargo::rerun-if-changed=schema/commands.tsv");

    let input = fs::read_to_string("schema/commands.tsv")
        .expect("read schema/commands.tsv");
    let count = input
        .lines()
        .filter(|line| !line.trim().is_empty())
        .count();
    let output = PathBuf::from(env::var("OUT_DIR").expect("Cargo must set OUT_DIR"));

    fs::write(
        output.join("generated.rs"),
        format!("pub const COMMAND_COUNT: usize = {count};\n"),
    )
    .expect("write generated file");
}
