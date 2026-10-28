use commandforge::{execute, exit_codes, Diagnostic, COMMANDS};

fn args(values: &[&str]) -> Vec<String> { values.iter().map(|value| (*value).to_owned()).collect() }

#[test]
fn catalog_order_is_deterministic() {
    assert_eq!(COMMANDS.iter().map(|item| item.name).collect::<Vec<_>>(), vec!["add", "slug", "repeat", "contains"]);
}

#[test]
fn add_and_repeat_use_generated_decoders() {
    assert_eq!(execute(&args(&["run", "add", "--left", "20", "--right", "22"])).unwrap().output, "42");
    assert_eq!(execute(&args(&["run", "repeat", "--text", "ha"])).unwrap().output, "ha");
    assert_eq!(execute(&args(&["run", "repeat", "--text", "ha", "--times", "3"])).unwrap().output, "hahaha");
}

#[test]
fn argument_failures_remain_typed() {
    let error = execute(&args(&["run", "add", "--left", "x", "--right", "2"])).unwrap_err();
    assert!(error.to_string().contains("invalid value `x`"));
}

#[test]
fn diagnostic_catalog_round_trips() {
    for &diagnostic in Diagnostic::ALL {
        assert_eq!(Diagnostic::from_code(diagnostic.code()), Some(diagnostic));
    }
}

#[test]
fn generated_exit_codes_are_available() {
    assert_eq!(exit_codes::EXIT_SUCCESS, 0);
    assert_eq!(exit_codes::exit_code_by_name("USAGE_FAILURE").unwrap().code, 2);
}
