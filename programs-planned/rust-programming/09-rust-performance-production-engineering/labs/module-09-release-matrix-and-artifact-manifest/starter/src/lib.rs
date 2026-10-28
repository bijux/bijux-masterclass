use std::collections::BTreeMap;

pub fn render(fields: BTreeMap<String, String>) -> String {
    fields
        .into_iter()
        .map(|(key, value)| format!("{key}={value}\n"))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fields_are_sorted() {
        let fields = BTreeMap::from([
            ("target".to_owned(), "x86_64".to_owned()),
            ("artifact".to_owned(), "app".to_owned()),
        ]);
        assert!(render(fields).starts_with("artifact=app\n"));
    }
}
