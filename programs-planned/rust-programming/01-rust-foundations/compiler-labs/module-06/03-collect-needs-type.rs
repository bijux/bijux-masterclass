// Predict before compiling.
fn main() {
    let doubled = [1, 2, 3].into_iter().map(|value| value * 2).collect();
    println!("{doubled:?}");
}
