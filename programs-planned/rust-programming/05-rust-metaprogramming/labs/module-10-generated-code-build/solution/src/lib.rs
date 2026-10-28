#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GeneratedCommand {
    pub name: &'static str,
    pub code: u16,
    pub help: &'static str,
}

include!(concat!(env!("OUT_DIR"), "/generated.rs"));

pub fn by_name(name: &str) -> Option<&'static GeneratedCommand> {
    COMMANDS.iter().find(|command| command.name == name)
}

pub fn by_code(code: u16) -> Option<&'static GeneratedCommand> {
    COMMANDS.iter().find(|command| command.code == code)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn generated_order_and_lookup_are_stable() {
        let names = COMMANDS
            .iter()
            .map(|command| command.name)
            .collect::<Vec<_>>();
        assert_eq!(names, vec!["list", "show"]);
        assert_eq!(by_name("show").expect("show command").code, 20);
        assert_eq!(
            by_code(10).expect("code 10").help,
            "List all records",
        );
    }
}
