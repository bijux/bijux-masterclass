// Predict before compiling.
pub struct Task { pub title: String }
fn main() {
    let mut task = Task { title: String::from("valid") };
    task.title.clear();
    assert!(!task.title.is_empty());
}
