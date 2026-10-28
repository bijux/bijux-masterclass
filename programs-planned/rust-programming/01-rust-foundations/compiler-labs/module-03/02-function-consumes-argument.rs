// Predict before compiling.
fn length(text: String) -> usize { text.len() }

fn main() {
    let title = String::from("ownership");
    let length = length(title);
    println!("{title}: {length}");
}
