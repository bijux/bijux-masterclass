//! Reference implementation for an exhaustive document workflow.

/// Nonzero document identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct DocumentId(u64);

impl DocumentId {
    /// Creates an identifier, rejecting zero.
    pub const fn new(value: u64) -> Option<Self> {
        if value == 0 {
            None
        } else {
            Some(Self(value))
        }
    }

    /// Returns the primitive value.
    pub const fn get(self) -> u64 {
        self.0
    }
}

/// Authoritative document lifecycle state.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    /// Editable and not submitted.
    Draft,
    /// Waiting for a review decision.
    InReview,
    /// Approved but not yet archived.
    Approved,
    /// Terminal archived state.
    Archived,
}

/// Operation requested against a document.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Transition {
    /// Submit a draft.
    Submit,
    /// Approve a document in review.
    Approve,
    /// Return a document in review to draft.
    Reject,
    /// Archive an approved document.
    Archive,
}

/// Document with private identity, title, and lifecycle state.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Document {
    id: DocumentId,
    title: String,
    state: State,
}

impl Document {
    /// Creates a draft document.
    pub fn new(id: DocumentId, title: String) -> Self {
        Self { id, title, state: State::Draft }
    }

    /// Returns the document ID.
    pub const fn id(&self) -> DocumentId {
        self.id
    }

    /// Borrows the title.
    pub fn title(&self) -> &str {
        &self.title
    }

    /// Returns the current state.
    pub const fn state(&self) -> State {
        self.state
    }

    /// Applies a legal transition and returns whether state changed.
    pub fn apply(&mut self, transition: Transition) -> bool {
        let next = match (self.state, transition) {
            (State::Draft, Transition::Submit) => State::InReview,
            (State::InReview, Transition::Approve) => State::Approved,
            (State::InReview, Transition::Reject) => State::Draft,
            (State::Approved, Transition::Archive) => State::Archived,
            _ => return false,
        };
        self.state = next;
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn identifier_rejects_zero() {
        assert_eq!(DocumentId::new(0), None);
        assert_eq!(DocumentId::new(1).map(DocumentId::get), Some(1));
    }

    #[test]
    fn constructor_establishes_draft_invariant() {
        let document = Document::new(DocumentId::new(7).expect("nonzero"), String::from("Design"));
        assert_eq!(document.id().get(), 7);
        assert_eq!(document.title(), "Design");
        assert_eq!(document.state(), State::Draft);
    }

    #[test]
    fn full_state_transition_matrix_is_covered() {
        let states = [State::Draft, State::InReview, State::Approved, State::Archived];
        let transitions = [
            Transition::Submit,
            Transition::Approve,
            Transition::Reject,
            Transition::Archive,
        ];

        for state in states {
            for transition in transitions {
                let expected = match (state, transition) {
                    (State::Draft, Transition::Submit) => Some(State::InReview),
                    (State::InReview, Transition::Approve) => Some(State::Approved),
                    (State::InReview, Transition::Reject) => Some(State::Draft),
                    (State::Approved, Transition::Archive) => Some(State::Archived),
                    _ => None,
                };
                let mut document = Document::new(
                    DocumentId::new(1).expect("nonzero"),
                    String::from("Matrix"),
                );
                document.state = state;
                let changed = document.apply(transition);
                assert_eq!(
                    changed,
                    expected.is_some(),
                    "state={state:?}, transition={transition:?}"
                );
                assert_eq!(document.state(), expected.unwrap_or(state));
            }
        }
    }

    #[test]
    fn rejected_transition_preserves_all_fields() {
        let mut document = Document::new(
            DocumentId::new(1).expect("nonzero"),
            String::from("Stable"),
        );
        let before = document.clone();
        assert!(!document.apply(Transition::Archive));
        assert_eq!(document, before);
    }
}
