pub struct OwnedTable {
    rows: Vec<Vec<String>>,
}

impl OwnedTable {
    pub fn parse(input: &str) -> Self {
        let rows = input
            .lines()
            .map(|line| line.split('\t').map(str::to_owned).collect())
            .collect();
        Self { rows }
    }

    pub fn rows(&self) -> &[Vec<String>] {
        &self.rows
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_owned_parser_preserves_fields() {
        let table = OwnedTable::parse("a\tb\nc\td");
        assert_eq!(table.rows()[0][1], "b");
    }
}
