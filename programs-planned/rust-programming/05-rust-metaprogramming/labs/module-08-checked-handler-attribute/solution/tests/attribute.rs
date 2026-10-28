use c5_lab08_handler_solution::checked_handler;

#[checked_handler(name = "echo", about = "Return text")]
#[inline]
pub fn echo(input: &str) -> Result<String, String> {
    Ok(input.to_owned())
}

#[test]
fn preserves_the_function_and_emits_typed_metadata() {
    assert_eq!(echo("x").expect("direct call"), "x");
    assert_eq!(ECHO_HANDLER.0, "echo");
    assert_eq!((ECHO_HANDLER.2)("y").expect("pointer call"), "y");
}
