// Predict before compiling.
mod model { pub struct Task { pub id: u64, title: String } }
fn main() { let _ = model::Task { id: 1, title: String::from("x") }; }
