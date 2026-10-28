#![forbid(unsafe_code)]
//! Reference design for the static-pipeline laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Submission { pub title: String, pub score: u8 }
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ValidationError { EmptyTitle, ScoreBelow(u8) }

pub trait Validate {
    type Input;
    type Error;
    fn validate(&self, input: &Self::Input) -> Result<(), Self::Error>;
}

pub struct NonEmptyTitle;
impl Validate for NonEmptyTitle {
    type Input = Submission; type Error = ValidationError;
    fn validate(&self, input: &Submission) -> Result<(), Self::Error> {
        if input.title.trim().is_empty() { Err(ValidationError::EmptyTitle) } else { Ok(()) }
    }
}

pub struct MinimumScore(pub u8);
impl Validate for MinimumScore {
    type Input = Submission; type Error = ValidationError;
    fn validate(&self, input: &Submission) -> Result<(), Self::Error> {
        if input.score < self.0 { Err(ValidationError::ScoreBelow(self.0)) } else { Ok(()) }
    }
}

pub struct Pipeline<A, B> { first: A, second: B }
impl<A, B> Pipeline<A, B> {
    pub fn new(first: A, second: B) -> Self { Self { first, second } }
    pub fn map_second<C>(self, second: C) -> Pipeline<A, C> { Pipeline { first: self.first, second } }
    pub fn validators(&self) -> impl Iterator<Item = &'static str> {
        ["first", "second"].into_iter()
    }
}
impl<A, B, I, E> Pipeline<A, B>
where A: Validate<Input = I, Error = E>, B: Validate<Input = I, Error = E> {
    pub fn validate(&self, input: &I) -> Result<(), E> {
        self.first.validate(input)?;
        self.second.validate(input)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn composes_static_validators() {
        let pipeline = Pipeline::new(NonEmptyTitle, MinimumScore(70));
        assert_eq!(pipeline.validate(&Submission { title: "Rust".into(), score: 80 }), Ok(()));
        assert_eq!(pipeline.validate(&Submission { title: "Rust".into(), score: 60 }), Err(ValidationError::ScoreBelow(70)));
    }
    #[test] fn map_changes_strategy_type() {
        let p = Pipeline::new(NonEmptyTitle, MinimumScore(70)).map_second(NonEmptyTitle);
        assert!(p.validate(&Submission { title: "x".into(), score: 0 }).is_ok());
    }
}
