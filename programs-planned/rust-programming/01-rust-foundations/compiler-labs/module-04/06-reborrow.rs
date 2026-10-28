// Predict before compiling.
fn append_mark(text: &mut String) { text.push('!'); }

fn main() {
    let mut title = String::from("safe");
    let access = &mut title;
    append_mark(access);
    println!("{access}");
    title.push('?');
    assert_eq!(title, "safe!?");
}
