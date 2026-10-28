#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Record {
    pub key: String,
    pub value: i64,
}

pub fn parse_line(line: &str) -> Result<Record, &'static str> {
    let (key, value) = line.split_once('\t').ok_or("expected two fields")?;
    let value = value.parse().map_err(|_| "invalid value")?;
    Ok(Record { key: key.to_owned(), value })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_one_record() {
        assert_eq!(
            parse_line("requests\t3"),
            Ok(Record { key: "requests".into(), value: 3 })
        );
    }
}
