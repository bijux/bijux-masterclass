pub trait Score {
    fn score(&self, input: u64) -> u64;
}

pub struct Add(pub u64);

impl Score for Add {
    fn score(&self, input: u64) -> u64 {
        input + self.0
    }
}

pub fn static_score<S: Score>(scorer: &S, input: u64) -> u64 {
    scorer.score(input)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_static_path_has_an_oracle() {
        assert_eq!(static_score(&Add(3), 4), 7);
    }
}
