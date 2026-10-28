//! Checked arithmetic over a minimally boxed recursive expression tree.
use std::fmt;
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Expr {
    Number(i64),
    Neg(Box<Expr>),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvalError {
    Overflow, DepthExceeded {
        limit: usize
    }
}
impl fmt::Display for EvalError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Overflow => write!(f, "arithmetic overflow"), Self::DepthExceeded {
                limit
            }
            => write!(f, "expression depth exceeds {limit}")
        }
    }
}
impl std::error::Error for EvalError {
}
impl Expr {
    pub fn number(value: i64) -> Self {
        Self::Number(value)
    }
    pub fn neg(value: Self) -> Self {
        Self::Neg(Box::new(value))
    }
    pub fn add(left: Self, right: Self) -> Self {
        Self::Add(Box::new(left), Box::new(right))
    }
    pub fn mul(left: Self, right: Self) -> Self {
        Self::Mul(Box::new(left), Box::new(right))
    }
    pub fn evaluate(&self) -> Result<i64, EvalError> {
        match self {
            Self::Number(value) => Ok(*value),
            Self::Neg(value) => value.evaluate()?.checked_neg().ok_or(EvalError::Overflow),
            Self::Add(left, right) => left.evaluate()?.checked_add(right.evaluate()?).ok_or(EvalError::Overflow),
            Self::Mul(left, right) => left.evaluate()?.checked_mul(right.evaluate()?).ok_or(EvalError::Overflow),
        }
    }
    pub fn node_count(&self) -> usize {
        match self {
            Self::Number(_) => 1,
            Self::Neg(value) => 1 + value.node_count(),
            Self::Add(left, right) | Self::Mul(left, right) => {
                1 + left.node_count() + right.node_count()
            }
        }
    }
    pub fn max_depth(&self) -> usize {
        match self {
            Self::Number(_) => 1,
            Self::Neg(value) => 1 + value.max_depth(),
            Self::Add(left, right) | Self::Mul(left, right) => {
                1 + left.max_depth().max(right.max_depth())
            }
        }
    }
    pub fn validate_depth(&self, limit: usize) -> Result<(), EvalError> {
        let mut stack = vec![(self, 1_usize)];
        while let Some((node, depth)) = stack.pop() {
            if depth > limit {
                return Err(EvalError::DepthExceeded {
                    limit
                });
            }
            match node {
                Self::Number(_) => {
                }
                Self::Neg(value) => stack.push((value, depth + 1)),
                Self::Add(left, right) | Self::Mul(left, right) => {
                    stack.push((left, depth + 1));
                    stack.push((right, depth + 1));
                }
            }
        }
        Ok(())
    }
    pub fn fold(self) -> Result<Self, EvalError> {
        match self {
            value @ Self::Number(_) => Ok(value),
            Self::Neg(value) => {
                match value.fold()? {
                    Self::Number(number) => Ok(Self::Number(number.checked_neg().ok_or(EvalError::Overflow)?)),
                    other => Ok(Self::Neg(Box::new(other))),
                }
            }
            Self::Add(left, right) => fold_binary(*left, *right, Self::Add, i64::checked_add),
            Self::Mul(left, right) => fold_binary(*left, *right, Self::Mul, i64::checked_mul),
        }
    }
}
fn fold_binary(
left: Expr,
right: Expr,
rebuild: fn(Box<Expr>, Box<Expr>) -> Expr,
operation: fn(i64, i64) -> Option<i64>,
) -> Result<Expr, EvalError> {
    let left = left.fold()?;
    let right = right.fold()?;
    match (&left, &right) {
        (Expr::Number(a), Expr::Number(b)) => Ok(Expr::Number(operation(*a, *b).ok_or(EvalError::Overflow)?)),
        _ => Ok(rebuild(Box::new(left), Box::new(right))),
    }
}
impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Number(value) => write!(f, "{value}"),
            Self::Neg(value) => write!(f, "(-{value})"),
            Self::Add(left, right) => write!(f, "({left} + {right})"),
            Self::Mul(left, right) => write!(f, "({left} * {right})"),
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn evaluates_and_renders() {
        let expression = Expr::mul(Expr::add(Expr::number(2), Expr::number(3)), Expr::neg(Expr::number(4)));
        assert_eq!(expression.evaluate(), Ok(-20));
        assert_eq!(expression.to_string(), "((2 + 3) * (-4))");
        assert_eq!(expression.node_count(), 6);
    }
    #[test]
    fn reports_overflow() {
        assert_eq!(Expr::add(Expr::number(i64::MAX), Expr::number(1)).evaluate(), Err(EvalError::Overflow));
    }
    #[test]
    fn folds_owned_tree() {
        let folded = Expr::add(Expr::number(10), Expr::mul(Expr::number(2), Expr::number(3))).fold();
        assert_eq!(folded, Ok(Expr::Number(16)));
    }
    #[test]
    fn iterative_depth_check_rejects_deep_input() {
        let mut expression = Expr::number(0);
        for _ in 0..100 {
            expression = Expr::neg(expression);
        }
        assert_eq!(expression.validate_depth(50), Err(EvalError::DepthExceeded {
            limit: 50
        }));
    }
}
