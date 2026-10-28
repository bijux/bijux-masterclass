#![forbid(unsafe_code)]
//! Starter for the associated-families laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct OwnedRow(pub Vec<String>);

pub struct TsvRows {
    rows: Vec<String>,
    next: usize,
}

impl TsvRows {
    pub fn new(input: &str) -> Self {
        Self { rows: input.lines().map(str::to_owned).collect(), next: 0 }
    }
    pub fn remaining(&self) -> usize { self.rows.len().saturating_sub(self.next) }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn constructs_source() { assert_eq!(TsvRows::new("a\tb\nc\td").remaining(), 2); }
}
