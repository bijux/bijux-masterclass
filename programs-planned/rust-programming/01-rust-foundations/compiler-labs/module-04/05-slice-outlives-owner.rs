// Predict before compiling.
fn main() {
    let word: &str;
    {
        let sentence = String::from("borrow safely");
        word = &sentence[..6];
    }
    println!("{word}");
}
