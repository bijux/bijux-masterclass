pub trait Stage {
    type Input;
    type Output;
    type Error;

    fn run(&self, input: Self::Input) -> Result<Self::Output, Self::Error>;
}

pub struct Chain<A, B> {
    first: A,
    second: B,
}

impl<A, B> Chain<A, B> {
    pub fn new(first: A, second: B) -> Self {
        Self { first, second }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum ChainError<A, B> {
    First(A),
    Second(B),
}

impl<A, B> Stage for Chain<A, B>
where
    A: Stage,
    B: Stage<Input = A::Output>,
{
    type Input = A::Input;
    type Output = B::Output;
    type Error = ChainError<A::Error, B::Error>;

    fn run(&self, input: Self::Input) -> Result<Self::Output, Self::Error> {
        let intermediate = self.first.run(input).map_err(ChainError::First)?;
        self.second
            .run(intermediate)
            .map_err(ChainError::Second)
    }
}

pub struct ParseU64;

impl Stage for ParseU64 {
    type Input = String;
    type Output = u64;
    type Error = std::num::ParseIntError;

    fn run(&self, input: String) -> Result<Self::Output, Self::Error> {
        input.parse()
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct TooLarge {
    pub value: u64,
    pub maximum: u64,
}

pub struct AtMost(pub u64);

impl Stage for AtMost {
    type Input = u64;
    type Output = u64;
    type Error = TooLarge;

    fn run(&self, input: u64) -> Result<Self::Output, Self::Error> {
        if input <= self.0 {
            Ok(input)
        } else {
            Err(TooLarge {
                value: input,
                maximum: self.0,
            })
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Overflow;

pub struct Double;

impl Stage for Double {
    type Input = u64;
    type Output = u64;
    type Error = Overflow;

    fn run(&self, input: u64) -> Result<Self::Output, Self::Error> {
        input.checked_mul(2).ok_or(Overflow)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn composes_equal_projections() {
        let pipeline = Chain::new(Chain::new(ParseU64, AtMost(100)), Double);
        assert_eq!(pipeline.run("21".into()), Ok(42));
    }

    #[test]
    fn preserves_first_error() {
        let pipeline = Chain::new(ParseU64, AtMost(100));
        assert!(matches!(
            pipeline.run("not-a-number".into()),
            Err(ChainError::First(_))
        ));
    }

    #[test]
    fn preserves_second_error() {
        let pipeline = Chain::new(ParseU64, AtMost(10));
        assert_eq!(
            pipeline.run("11".into()),
            Err(ChainError::Second(TooLarge {
                value: 11,
                maximum: 10,
            }))
        );
    }
}
