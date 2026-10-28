// Predict before compiling.
fn first(values: &[u64]) -> Result<u64, &'static str> {
    let value = values.first()?;
    Ok(*value)
}
fn main() {}
