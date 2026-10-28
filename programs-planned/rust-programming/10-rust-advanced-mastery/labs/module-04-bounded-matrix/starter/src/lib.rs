#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct BoundedIndex<const N: usize>(usize);

impl<const N: usize> BoundedIndex<N> {
    pub fn new(value: usize) -> Option<Self> {
        (value < N).then_some(Self(value))
    }

    pub fn get(self) -> usize {
        self.0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn witness_rejects_the_first_invalid_index() {
        assert!(BoundedIndex::<3>::new(2).is_some());
        assert!(BoundedIndex::<3>::new(3).is_none());
    }
}
