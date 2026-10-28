// Predict before compiling.
fn main() {
    let mut values = vec![String::from("one")];
    let first = &values[0];
    values.push(String::from("two"));
    println!("{first}");
}
