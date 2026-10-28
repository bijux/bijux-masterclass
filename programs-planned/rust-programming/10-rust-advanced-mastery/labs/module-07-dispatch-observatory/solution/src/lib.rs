pub trait Score {
    fn score(&self, input: u64) -> Option<u64>;
}

#[derive(Clone, Copy, Debug)]
pub struct Add(pub u64);

#[derive(Clone, Copy, Debug)]
pub struct Multiply(pub u64);

impl Score for Add {
    fn score(&self, input: u64) -> Option<u64> {
        input.checked_add(self.0)
    }
}

impl Score for Multiply {
    fn score(&self, input: u64) -> Option<u64> {
        input.checked_mul(self.0)
    }
}

#[derive(Clone, Copy, Debug)]
pub enum BuiltIn {
    Add(Add),
    Multiply(Multiply),
}

impl Score for BuiltIn {
    fn score(&self, input: u64) -> Option<u64> {
        match self {
            Self::Add(scorer) => scorer.score(input),
            Self::Multiply(scorer) => scorer.score(input),
        }
    }
}

pub fn static_score<S: Score>(scorer: &S, input: u64) -> Option<u64> {
    scorer.score(input)
}

pub fn dynamic_score(scorer: &dyn Score, input: u64) -> Option<u64> {
    scorer.score(input)
}

pub fn paths_agree<S>(scorer: S, built_in: BuiltIn, input: u64) -> bool
where
    S: Score + Clone + 'static,
{
    let erased: Box<dyn Score> = Box::new(scorer.clone());
    static_score(&scorer, input) == built_in.score(input)
        && built_in.score(input) == dynamic_score(erased.as_ref(), input)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_add_paths_share_an_oracle() {
        for input in 0..100 {
            assert!(paths_agree(Add(3), BuiltIn::Add(Add(3)), input));
        }
    }

    #[test]
    fn all_multiply_paths_share_an_oracle() {
        for input in 0..100 {
            assert!(paths_agree(
                Multiply(7),
                BuiltIn::Multiply(Multiply(7)),
                input
            ));
        }
    }

    #[test]
    fn overflow_policy_is_identical() {
        assert!(paths_agree(Add(1), BuiltIn::Add(Add(1)), u64::MAX));
    }
}
