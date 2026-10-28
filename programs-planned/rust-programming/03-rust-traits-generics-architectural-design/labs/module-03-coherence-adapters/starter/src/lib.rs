#![forbid(unsafe_code)]
//! Starter for the coherence-adapters laboratory.

pub mod vendor {
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub struct Bytes(pub Vec<u8>);
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub struct Record { pub key: String }
}

pub struct HexBytes(pub vendor::Bytes);

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn wrapper_is_distinct() { let _ = HexBytes(vendor::Bytes(vec![1, 2])); }
}
