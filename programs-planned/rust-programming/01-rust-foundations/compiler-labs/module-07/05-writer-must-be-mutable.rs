// Predict before compiling.
use std::io::{self, Write};
fn emit<W: Write>(writer: &W) -> io::Result<()> {
    writeln!(writer, "record")
}
fn main() {}
