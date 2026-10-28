// Predict before compiling.
fn consume(value: String) { drop(value); }

fn main() {
    let title = String::from("repeat");
    for _ in 0..2 {
        consume(title);
    }
}
