// Predict before compiling.
fn main() {
    let values = [1, 2, 3];
    let total = 0;
    for value in &values {
        total += value;
    }
    println!("{total}");
}
