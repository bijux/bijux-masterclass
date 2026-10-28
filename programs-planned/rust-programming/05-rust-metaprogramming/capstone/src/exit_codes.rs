#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ExitCodeRecord {
    pub name: &'static str,
    pub code: i32,
    pub description: &'static str,
}

include!(concat!(env!("OUT_DIR"), "/exit_codes.rs"));

pub fn exit_code_by_name(name: &str) -> Option<&'static ExitCodeRecord> {
    EXIT_CODES.iter().find(|row| row.name == name)
}
