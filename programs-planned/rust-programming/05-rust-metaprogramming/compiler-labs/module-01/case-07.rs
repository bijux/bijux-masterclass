const COMMANDS: &[(&str, &str)] = &[("list", "list values"), ("show", "show one value")];
fn main() { assert_eq!(COMMANDS[0].0, "list"); }
