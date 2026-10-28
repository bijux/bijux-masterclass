#![forbid(unsafe_code)]
//! Starter for the static-pipeline laboratory.

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Submission { pub title: String, pub score: u8 }

pub struct Pipeline<A, B> { pub first: A, pub second: B }
impl<A, B> Pipeline<A, B> {
    pub fn new(first: A, second: B) -> Self { Self { first, second } }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn constructs_pipeline() { let _ = Pipeline::new(1u8, "two"); }
}
