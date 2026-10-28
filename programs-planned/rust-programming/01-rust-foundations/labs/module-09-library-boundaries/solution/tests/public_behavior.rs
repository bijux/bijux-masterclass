use rust_foundations_lab_09_library_boundaries::{Command, Registry, execute, parse_command};

#[test]
fn consumer_can_run_a_multi_step_session_without_representation_access() {
    let mut registry = Registry::new();
    let add_first = parse_command(&[String::from("add"), String::from("alpha")]).expect("parse");
    let add_second = parse_command(&[String::from("add"), String::from("beta")]).expect("parse");
    execute(&mut registry, add_first).expect("add");
    execute(&mut registry, add_second).expect("add");
    let listed = execute(&mut registry, Command::List).expect("list");
    assert_eq!(listed.output(), "1: alpha\n2: beta");
    assert!(!listed.changed());
}

#[test]
fn public_errors_preserve_behavioral_meaning() {
    let mut registry = Registry::new();
    let error = execute(
        &mut registry,
        Command::Remove("9".parse().expect("valid ID text")),
    )
    .expect_err("missing");
    assert_eq!(error.to_string(), "entry 9 was not found");
}
