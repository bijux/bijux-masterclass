// Predict before compiling.
fn main() {
    let mut values = vec![String::from("one")];
    let matches: Vec<&String> = values.iter().filter(|v| v.len() > 2).collect();
    values.push(String::from("two"));
    println!("{}", matches[0]);
}
