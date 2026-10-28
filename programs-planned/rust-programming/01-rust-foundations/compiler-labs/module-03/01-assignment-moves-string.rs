// Predict before compiling.
fn main() {
    let title = String::from("parse records");
    let archived = title;
    println!("{title}");
    drop(archived);
}
