mod build_support;

use build_support::{parse, render, write_generated};
use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    println!("cargo::rerun-if-changed=schema/commands.tsv");
    println!("cargo::rerun-if-changed=build_support.rs");

    let input = fs::read_to_string("schema/commands.tsv")
        .unwrap_or_else(|error| panic!("cannot read schema/commands.tsv: {error}"));
    let rows = parse(&input)
        .unwrap_or_else(|error| panic!("invalid command schema: {error}"));
    let generated = render(&rows);
    let output = PathBuf::from(env::var("OUT_DIR").expect("Cargo must set OUT_DIR"));
    let destination = output.join("generated.rs");

    write_generated(&destination, &generated).unwrap_or_else(|error| {
        panic!("cannot replace {}: {error}", destination.display())
    });
}
