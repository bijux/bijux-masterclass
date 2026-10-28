// Predict before compiling.
fn first(values: &[u64]) -> u64 {
    let Some(value) = values.first() else { 0 };
    *value
}
fn main() { println!("{}", first(&[])); }
