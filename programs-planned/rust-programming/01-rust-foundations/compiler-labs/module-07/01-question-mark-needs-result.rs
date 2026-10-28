// Predict before compiling.
fn parse() -> u64 {
    let value = "42".parse::<u64>()?;
    value
}
fn main() { println!("{}", parse()); }
