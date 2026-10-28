#![forbid(unsafe_code)]
//! Starter for the contract-boundaries laboratory.

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct Money(u64);

impl Money {
    pub const fn from_cents(cents: u64) -> Self { Self(cents) }
    pub const fn cents(self) -> u64 { self.0 }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Percentage(u8);

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct InvalidPercentage;

impl Percentage {
    pub fn new(value: u8) -> Result<Self, InvalidPercentage> {
        (value <= 100).then_some(Self(value)).ok_or(InvalidPercentage)
    }
    pub const fn get(self) -> u8 { self.0 }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn percentage_rejects_values_above_one_hundred() {
        assert_eq!(Percentage::new(101), Err(InvalidPercentage));
    }
}
