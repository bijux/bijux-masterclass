fn call_once<F>(function: F) -> String where F: FnOnce() -> String { function() }
fn main() {
    let token = String::from("token");
    let output = call_once(move || token);
    assert_eq!(output, "token");
}
