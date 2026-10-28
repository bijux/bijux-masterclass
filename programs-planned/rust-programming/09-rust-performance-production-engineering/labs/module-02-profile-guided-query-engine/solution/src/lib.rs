use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Document {
    pub id: u64,
    pub body: String,
}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct QueryCounters {
    pub documents_considered: usize,
    pub candidate_documents: usize,
    pub token_comparisons: usize,
}

#[derive(Debug)]
pub struct QueryEngine {
    documents: Vec<Document>,
    postings: BTreeMap<String, Vec<usize>>,
}

impl QueryEngine {
    pub fn build(documents: Vec<Document>) -> Self {
        let mut postings: BTreeMap<String, Vec<usize>> = BTreeMap::new();
        for (index, document) in documents.iter().enumerate() {
            let seen: BTreeSet<_> = document.body.split_whitespace().collect();
            for token in seen {
                postings.entry(token.to_owned()).or_default().push(index);
            }
        }
        Self { documents, postings }
    }

    pub fn search(&self, term: &str) -> (Vec<&Document>, QueryCounters) {
        let Some(indices) = self.postings.get(term) else {
            return (Vec::new(), QueryCounters::default());
        };
        let results = indices.iter().map(|&index| &self.documents[index]).collect();
        (
            results,
            QueryCounters {
                documents_considered: indices.len(),
                candidate_documents: indices.len(),
                token_comparisons: 0,
            },
        )
    }

    pub fn search_oracle(&self, term: &str) -> (Vec<&Document>, QueryCounters) {
        let mut counters = QueryCounters::default();
        let results = self
            .documents
            .iter()
            .filter(|document| {
                counters.documents_considered += 1;
                document.body.split_whitespace().any(|word| {
                    counters.token_comparisons += 1;
                    word == term
                })
            })
            .collect();
        (results, counters)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn documents() -> Vec<Document> {
        vec![
            Document { id: 3, body: "rust production engineering".into() },
            Document { id: 1, body: "measurement before optimization".into() },
            Document { id: 2, body: "rust rust profiling".into() },
        ]
    }

    #[test]
    fn index_matches_oracle_and_preserves_source_order() {
        let engine = QueryEngine::build(documents());
        for term in ["rust", "optimization", "missing"] {
            let (indexed, _) = engine.search(term);
            let (oracle, _) = engine.search_oracle(term);
            let indexed_ids: Vec<_> = indexed.iter().map(|doc| doc.id).collect();
            let oracle_ids: Vec<_> = oracle.iter().map(|doc| doc.id).collect();
            assert_eq!(indexed_ids, oracle_ids);
        }
    }

    #[test]
    fn repeated_token_adds_one_posting_per_document() {
        let engine = QueryEngine::build(documents());
        let (results, counters) = engine.search("rust");
        assert_eq!(results.len(), 2);
        assert_eq!(counters.candidate_documents, 2);
    }

    #[test]
    fn indexed_path_avoids_full_scan_for_missing_term() {
        let engine = QueryEngine::build(documents());
        let (_, indexed) = engine.search("absent");
        let (_, oracle) = engine.search_oracle("absent");
        assert_eq!(indexed.documents_considered, 0);
        assert_eq!(oracle.documents_considered, 3);
    }
}
