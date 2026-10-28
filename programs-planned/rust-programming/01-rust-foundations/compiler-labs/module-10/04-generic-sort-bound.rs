// Predict before compiling.
fn sorted<T>(values: &[T]) -> Vec<&T> {
    let mut output: Vec<_> = values.iter().collect();
    output.sort();
    output
}
fn main() {}
