fn main() {
    let (mut ok, mut bad) = (Vec::new(), Vec::new());
    for item in [Ok(1), Err("a"), Ok(2), Err("b")] {
        match item { Ok(value) => ok.push(value), Err(error) => bad.push(error) }
    }
    assert_eq!(ok, vec![1, 2]); assert_eq!(bad, vec!["a", "b"]);
}
