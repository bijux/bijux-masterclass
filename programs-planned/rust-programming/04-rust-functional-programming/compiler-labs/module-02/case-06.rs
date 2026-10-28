fn main() {
    let mut input = ["a", "STOP", "b"].into_iter().peekable();
    assert_eq!(input.peek(), Some(&"a"));
    assert_eq!(input.next(), Some("a"));
    assert_eq!(input.peek(), Some(&"STOP"));
}
