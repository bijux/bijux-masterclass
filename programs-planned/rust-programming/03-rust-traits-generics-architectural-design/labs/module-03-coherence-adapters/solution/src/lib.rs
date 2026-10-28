#![forbid(unsafe_code)]
//! Reference design for the coherence-adapters laboratory.

pub mod vendor {
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub struct Bytes(pub Vec<u8>);
    #[derive(Clone, Debug, PartialEq, Eq)]
    pub struct Record { pub key: String }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct HexBytes(pub vendor::Bytes);
impl std::fmt::Display for HexBytes {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for byte in &self.0.0 { write!(f, "{byte:02x}")?; }
        Ok(())
    }
}

pub trait RecordExt {
    fn normalized_key(&self) -> String;
}
impl RecordExt for vendor::Record {
    fn normalized_key(&self) -> String { self.key.trim().to_ascii_lowercase() }
}

mod private {
    pub trait Sealed {}
}

pub trait ValidRecord: private::Sealed {
    fn key(&self) -> &str;
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CheckedRecord(vendor::Record);
impl CheckedRecord {
    pub fn new(record: vendor::Record) -> Result<Self, EmptyKey> {
        if record.key.trim().is_empty() { Err(EmptyKey) } else { Ok(Self(record)) }
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct EmptyKey;
impl private::Sealed for CheckedRecord {}
impl ValidRecord for CheckedRecord { fn key(&self) -> &str { &self.0.key } }

pub trait ValidRecordExt: ValidRecord {
    fn key_len(&self) -> usize { self.key().chars().count() }
}
impl<T: ValidRecord + ?Sized> ValidRecordExt for T {}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn newtype_owns_display_semantics() {
        assert_eq!(HexBytes(vendor::Bytes(vec![0x0a, 0xff])).to_string(), "0aff");
    }
    #[test] fn extension_is_opt_in_behavior() {
        let record = vendor::Record { key: " A-B ".into() };
        assert_eq!(record.normalized_key(), "a-b");
    }
    #[test] fn sealed_value_preserves_validation() {
        let checked = CheckedRecord::new(vendor::Record { key: "x".into() }).expect("valid");
        assert_eq!(checked.key_len(), 1);
    }
}
