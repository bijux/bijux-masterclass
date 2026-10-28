// Predict before compiling.
enum Command { Add { title: String } }
fn main() {
    let title = String::from("Ship");
    let command = Command::Add { title };
    println!("{title}");
    drop(command);
}
