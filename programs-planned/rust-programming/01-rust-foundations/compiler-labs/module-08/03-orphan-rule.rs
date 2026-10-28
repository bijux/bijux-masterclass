// Predict before compiling.
use std::fmt;
impl fmt::Display for Vec<u64> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { write!(f, "{} values", self.len()) }
}
fn main() {}
