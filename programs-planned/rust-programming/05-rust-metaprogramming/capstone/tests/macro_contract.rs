use commandforge::{CommandArgs, handlers::{AddArgs, RepeatArgs}};

fn values(items: &[&str]) -> Vec<String> { items.iter().map(|item| (*item).to_owned()).collect() }

#[test]
fn derive_exposes_usage_and_argument_metadata() {
    assert_eq!(AddArgs::USAGE, "--left <value> --right <value>");
    assert_eq!(AddArgs::ARGUMENTS.len(), 2);
    assert!(AddArgs::ARGUMENTS.iter().all(|argument| argument.required));
    assert!(RepeatArgs::ARGUMENTS.iter().any(|argument| !argument.required));
}

#[test]
fn duplicate_flags_are_rejected() {
    let error = AddArgs::decode(&values(&["--left", "1", "--left", "2", "--right", "3"]))
        .unwrap_err();
    assert!(error.to_string().contains("more than once"));
}

#[test]
fn unknown_flags_are_rejected() {
    let error = AddArgs::decode(&values(&["--left", "1", "--right", "2", "--extra", "3"]))
        .unwrap_err();
    assert!(error.to_string().contains("unknown argument"));
}

commandforge::command_catalog! {
    static TEST_COMMANDS;
    fn find_test_command;
    {
        "sum" => commandforge::handlers::ADD_HANDLER;
    }
}

#[test]
fn catalog_item_names_are_explicit_and_do_not_collide() {
    assert_eq!(TEST_COMMANDS.len(), 1);
    assert_eq!(find_test_command("sum").map(|command| command.name), Some("sum"));
    assert!(find_test_command("missing").is_none());
}

