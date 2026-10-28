// Predict before compiling.
fn main() {
    let title = String::from("temporary");
    drop(title);
    println!("{title}");
}
