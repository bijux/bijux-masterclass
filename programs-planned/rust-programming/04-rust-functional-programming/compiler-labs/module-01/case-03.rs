fn main() {
    let text = String::from("abc");
    let length = move || text.len();
    assert_eq!(length(), 3);
    assert_eq!(length(), 3);
}
