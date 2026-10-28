// Predict before compiling.
fn main() {
    let mut values = [1, 2];
    let first = &mut values[0];
    let second = &mut values[1];
    *first += *second;
}
