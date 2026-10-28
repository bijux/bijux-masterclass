// Predict before compiling.
struct Task { done: bool }
impl Task { fn complete(&self) { self.done = true; } }
fn main() { let task = Task { done: false }; task.complete(); }
