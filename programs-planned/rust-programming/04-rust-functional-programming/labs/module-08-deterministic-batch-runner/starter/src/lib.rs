#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Input {
    pub name: String,
    pub due: u64,
    pub valid: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Scheduled {
    pub id: u64,
    pub name: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Action {
    Write { path: String, contents: String },
    Notify { message: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Analysis {
    pub scheduled: Vec<Scheduled>,
    pub rejected: Vec<String>,
}

#[cfg(test)]
mod tests {
    use super::{Action, Analysis, Input};

    #[test]
    fn starter_keeps_analysis_separate_from_effect_actions() {
        let input = Input { name: "job".to_owned(), due: 10, valid: true };
        let analysis = Analysis::default();
        let action = Action::Write {
            path: "jobs/1.txt".to_owned(),
            contents: input.name,
        };
        assert!(analysis.scheduled.is_empty());
        assert!(matches!(action, Action::Write { .. }));
    }
}
