// Predict before compiling.
use std::io::{self, Write};
fn emit<W: Write>(mut writer: W) -> io::Result<()> { writeln!(writer, "row") }
fn report(output: Vec<u8>) -> io::Result<Vec<u8>> { emit(output)?; emit(output)?; Ok(output) }
fn main() {}
