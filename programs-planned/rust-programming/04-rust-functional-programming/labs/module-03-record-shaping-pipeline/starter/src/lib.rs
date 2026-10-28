#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Survey {
    pub payload: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Observation {
    pub record_index: usize,
    pub field_index: usize,
    pub label: String,
    pub score: i64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ShapeError {
    LengthMismatch { labels: usize, scores: usize },
    MissingLabel { field: usize },
    MissingScore { field: usize },
    InvalidScore { field: usize, value: String },
}

#[cfg(test)]
mod tests {
    use super::Survey;

    #[test]
    fn absence_is_represented_without_a_sentinel_string() {
        let survey = Survey { payload: None };
        assert!(survey.payload.is_none());
    }
}
