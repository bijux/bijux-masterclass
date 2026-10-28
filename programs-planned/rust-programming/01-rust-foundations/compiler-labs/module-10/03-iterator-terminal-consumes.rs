// Predict before compiling.
fn main() {
    let values = [1, 2, 3];
    let mut matches = values.iter().filter(|v| **v > 1);
    let count = matches.count();
    let first = matches.next();
    println!("{count} {first:?}");
}
