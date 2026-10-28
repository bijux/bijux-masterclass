// Predict before compiling.
fn title() -> &str {
    let value = String::from("local");
    &value
}

fn main() { println!("{}", title()); }
