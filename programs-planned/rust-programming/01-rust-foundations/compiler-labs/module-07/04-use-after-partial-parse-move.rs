// Predict before compiling.
fn main() {
    let input = String::from("42");
    let parsed: u64 = input.parse().unwrap();
    drop(input);
    println!("{parsed}");
}
