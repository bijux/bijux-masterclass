// Predict before compiling.
fn main() {
    let result = loop {
        if ready() { break 7; }
        break "seven";
    };
    println!("{result:?}");
}

fn ready() -> bool { false }
