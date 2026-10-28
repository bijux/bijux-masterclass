// Predict before compiling.
fn main() {
    let mut title = String::from("task");
    let view = &title;
    title.push('!');
    println!("{view}");
}
