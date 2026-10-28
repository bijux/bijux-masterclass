fn main() {
    let raw = Some("7");
    let parsed: Result<Option<i32>, _> = raw.map(str::parse).transpose();
    assert_eq!(parsed, Ok(Some(7)));
}
