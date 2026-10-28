// Predict before compiling.
fn render<T>(value: T) -> String { format!("{value}") }
fn main() { println!("{}", render(3)); }
