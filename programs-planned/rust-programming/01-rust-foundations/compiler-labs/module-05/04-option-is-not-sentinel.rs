// Predict before compiling.
fn find(values: &[u64], wanted: u64) -> Option<usize> {
    values.iter().position(|value| *value == wanted)
}

fn main() {
    let index: usize = find(&[4, 5], 9);
    println!("{index}");
}
