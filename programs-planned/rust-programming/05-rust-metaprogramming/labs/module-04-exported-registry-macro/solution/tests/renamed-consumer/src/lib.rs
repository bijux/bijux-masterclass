#![forbid(unsafe_code)]

use renamed_registry::{command_registry, find};

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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exported_macro_survives_dependency_renaming_and_shadowing() {
        let entry = find(nested::COMMANDS, "echo").expect("registered command");
        assert_eq!((entry.handler)("payload"), "payload");
        let _shadow = Entry;
    }
}
