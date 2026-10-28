#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Document {
    pub id: u64,
    pub body: String,
}

pub fn search<'a>(documents: &'a [Document], term: &str) -> Vec<&'a Document> {
    documents
        .iter()
        .filter(|document| document.body.split_whitespace().any(|word| word == term))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn search_preserves_source_order() {
        let documents = vec![
            Document { id: 2, body: "rust systems".into() },
            Document { id: 1, body: "rust performance".into() },
        ];
        let ids: Vec<_> = search(&documents, "rust").into_iter().map(|d| d.id).collect();
        assert_eq!(ids, vec![2, 1]);
    }
}
