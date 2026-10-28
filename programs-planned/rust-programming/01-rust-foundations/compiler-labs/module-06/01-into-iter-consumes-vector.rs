// Predict before compiling.
fn main() {
    let values = vec![String::from("a"), String::from("b")];
    for value in values { println!("{value}"); }
    println!("{}", values.len());
}
