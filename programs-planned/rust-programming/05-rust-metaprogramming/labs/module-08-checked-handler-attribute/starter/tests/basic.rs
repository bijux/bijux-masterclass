use c5_lab08_handler_starter::checked_handler;

#[checked_handler]
fn echo(input: &str) -> Result<String, String> {
    Ok(input.to_owned())
}

#[test]
fn baseline_preserves_the_function() {
    assert_eq!(echo("x").expect("handler succeeds"), "x");
}
