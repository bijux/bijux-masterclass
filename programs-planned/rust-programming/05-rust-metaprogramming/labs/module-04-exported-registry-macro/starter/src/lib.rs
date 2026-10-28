#![forbid(unsafe_code)]

#[derive(Clone, Copy)]
pub struct Entry {
    pub name: &'static str,
    pub handler: fn(&str) -> String,
}

impl Entry {
    pub const fn new(
        name: &'static str,
        handler: fn(&str) -> String,
    ) -> Self {
        Self { name, handler }
    }
}

pub fn find(entries: &[Entry], name: &str) -> Option<Entry> {
    entries.iter().copied().find(|entry| entry.name == name)
}
