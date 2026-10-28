// Predict before compiling.
#[derive(Debug)]
enum Command { Add { title: String }, Help }

fn main() {
    let command = Command::Add { title: String::from("task") };
    if let Command::Add { title } = command { println!("{title}"); }
    println!("{command:?}");
}
