pub trait Stage {
    type Input;
    type Output;
    type Error;

    fn run(&self, input: Self::Input) -> Result<Self::Output, Self::Error>;
}

pub struct Identity<T>(std::marker::PhantomData<T>);

impl<T> Identity<T> {
    pub fn new() -> Self {
        Self(std::marker::PhantomData)
    }
}

impl<T> Default for Identity<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> Stage for Identity<T> {
    type Input = T;
    type Output = T;
    type Error = std::convert::Infallible;

    fn run(&self, input: T) -> Result<T, Self::Error> {
        Ok(input)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_stage_preserves_the_value() {
        assert_eq!(Identity::<u64>::new().run(7), Ok(7));
    }
}
