// Predict before compiling.
mod domain {
    pub struct TaskId(u64);
}

fn main() {
    let _ = domain::TaskId(1);
}
