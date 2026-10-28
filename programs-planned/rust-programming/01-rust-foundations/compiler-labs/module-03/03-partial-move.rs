// Predict before compiling.
fn main() {
    let record = (7_u64, String::from("task"));
    let title = record.1;
    println!("{record:?} {title}");
}
