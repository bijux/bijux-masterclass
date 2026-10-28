//! Finite recursive-expression baseline.
//!
//! Checked evaluation, analysis, depth policy, additional variants, and
//! consuming folding remain the learner's work.

/// Recursively owned arithmetic expression.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Expr {
    /// Integer leaf.
    Number(i64),
    /// Sum of two owned child expressions.
    Add(Box<Expr>, Box<Expr>),
}

impl Expr {
    /// Constructs an integer leaf.
    pub const fn number(value: i64) -> Self {
        Self::Number(value)
    }

    /// Constructs an addition node by boxing only recursive children.
    pub fn add(left: Self, right: Self) -> Self {
        Self::Add(Box::new(left), Box::new(right))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_representation_is_finite_and_owned() {
        let expression = Expr::add(Expr::number(1), Expr::number(2));
        assert_eq!(
            expression,
            Expr::Add(Box::new(Expr::Number(1)), Box::new(Expr::Number(2)))
        );
    }
}
