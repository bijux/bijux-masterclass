// Predict before compiling.
fn classify(value: i32) -> &'static str {
    if value < 0 {
        "negative"
    } else {
        "positive";
    }
}

fn main() { println!("{}", classify(1)); }
