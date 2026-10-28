#![forbid(unsafe_code)]
//! Reference design for the contract-boundaries laboratory.

pub const DOMAIN_PRICE_LIMIT: u64 = 10_000_000_00;

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

/// A product whose base price is valid within the course domain.
pub trait Priced {
    fn base_price(&self) -> Money;
    fn is_free(&self) -> bool { self.base_price().cents() == 0 }
}

#[derive(Debug)]
pub struct Book { pub unit_cents: u64 }
#[derive(Debug)]
pub struct CourseLicense { pub seat_cents: u64, pub seats: u32 }
#[derive(Debug)]
pub struct SupportPlan { pub monthly_cents: u64, pub months: u8 }

impl Priced for Book {
    fn base_price(&self) -> Money { Money::from_cents(self.unit_cents.min(DOMAIN_PRICE_LIMIT)) }
}
impl Priced for CourseLicense {
    fn base_price(&self) -> Money {
        Money::from_cents(self.seat_cents.saturating_mul(u64::from(self.seats)).min(DOMAIN_PRICE_LIMIT))
    }
}
impl Priced for SupportPlan {
    fn base_price(&self) -> Money {
        Money::from_cents(self.monthly_cents.saturating_mul(u64::from(self.months)).min(DOMAIN_PRICE_LIMIT))
    }
}

pub fn discounted<P: Priced>(product: &P, discount: Percentage) -> Money {
    let base = product.base_price().cents();
    let reduction = base.saturating_mul(u64::from(discount.get())) / 100;
    Money::from_cents(base - reduction)
}

pub fn invoice_line<P>(label: &str, product: &P) -> String
where P: Priced {
    format!("{label}: {} cents", product.base_price().cents())
}

#[cfg(test)]
mod tests {
    use super::*;
    fn assert_price_laws<T: Priced>(value: &T) {
        assert!(value.base_price().cents() <= DOMAIN_PRICE_LIMIT);
        assert_eq!(value.base_price(), value.base_price());
    }
    #[test] fn laws_hold_for_all_products() {
        assert_price_laws(&Book { unit_cents: 2_500 });
        assert_price_laws(&CourseLicense { seat_cents: 1_000, seats: 3 });
        assert_price_laws(&SupportPlan { monthly_cents: 500, months: 12 });
    }
    #[test] fn discount_is_separate_policy() {
        let p = Percentage::new(20).expect("valid");
        assert_eq!(discounted(&Book { unit_cents: 2_500 }, p).cents(), 2_000);
    }
    #[test] fn default_method_is_derived_from_base_price() {
        assert!(Book { unit_cents: 0 }.is_free());
    }
}
