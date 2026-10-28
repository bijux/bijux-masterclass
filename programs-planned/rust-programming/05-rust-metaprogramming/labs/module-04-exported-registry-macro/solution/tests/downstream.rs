use c5_lab04_registry_solution::{command_registry, find};

struct Entry;

fn echo(input: &str) -> String {
    input.to_owned()
}

mod nested {
    use super::*;

    command_registry! {
        pub static COMMANDS {
            "echo" => crate::echo;
        }
    }
}

#[test]
fn expansion_uses_the_definition_crates_entry_type() {
    let entry = find(nested::COMMANDS, "echo").expect("registered command");
    assert_eq!((entry.handler)("x"), "x");
    let _shadow = Entry;
}

#[test]
fn registry_preserves_authored_order() {
    fn upper(input: &str) -> String {
        input.to_ascii_uppercase()
    }

    command_registry! {
        static LOCAL {
            "echo" => echo;
            "upper" => upper;
        }
    }

    let names = LOCAL.iter().map(|entry| entry.name).collect::<Vec<_>>();
    assert_eq!(names, vec!["echo", "upper"]);
}
