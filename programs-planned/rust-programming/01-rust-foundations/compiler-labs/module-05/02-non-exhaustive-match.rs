// Predict before compiling.
enum Status { Todo, Doing, Done, Paused }

fn label(status: Status) -> &'static str {
    match status {
        Status::Todo => "todo",
        Status::Doing => "doing",
        Status::Done => "done",
    }
}

fn main() { println!("{}", label(Status::Paused)); }
