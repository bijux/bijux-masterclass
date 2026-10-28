mod build_support;

use build_support::{parse, render, write_generated};
use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    println!("cargo::rerun-if-changed=config/exit_codes.tsv");
    println!("cargo::rerun-if-changed=build_support.rs");

    let input = fs::read_to_string("config/exit_codes.tsv")
        .unwrap_or_else(|error| panic!("cannot read config/exit_codes.tsv: {error}"));
    let rows = parse(&input)
        .unwrap_or_else(|error| panic!("invalid exit-code table: {error}"));
    let generated = render(&rows);

    let output_dir = PathBuf::from(env::var("OUT_DIR").expect("Cargo must set OUT_DIR"));
    let destination = output_dir.join("exit_codes.rs");
    write_generated(&destination, &generated)
        .unwrap_or_else(|error| panic!("cannot replace {}: {error}", destination.display()));
}
