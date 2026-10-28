// Predict before compiling.
fn label(high: bool) -> &'static str {
    if high { "high" } else { 0 }
}

fn main() {
    println!("{}", label(true));
}
