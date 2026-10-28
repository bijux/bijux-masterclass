// Predict before compiling.
fn visible(values: &[u64], all: bool) -> impl Iterator<Item = &u64> {
    if all { values.iter() } else { values.iter().filter(|value| **value > 0) }
}
fn main() {}
