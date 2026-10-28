//! Safe layout observations separated from portable guarantees.
use std::mem::{
    align_of, size_of, size_of_val
};
use std::rc::Rc;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Classification {
    Guaranteed, TargetConditioned, Observed
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Observation {
    pub name: &'static str,
    pub value: usize,
    pub classification: Classification,
    pub note: &'static str,
}
#[repr(C)]
pub struct CHeader {
    pub kind: u8, pub length: u32, pub flags: u16
}
#[repr(transparent)]
pub struct DocumentId(pub u64);
pub struct Marker;
pub fn report() -> Vec<Observation> {
    let text = String::from("rust");
    let boxed: Box<[u32]> = vec![1_u32, 2, 3].into_boxed_slice();
    let shared: Rc<str> = Rc::from("shared");
    vec![
    obs("u32 size", size_of::<u32>(), Classification::Guaranteed, "primitive size is defined by its width"),
    obs(
        "CHeader size",
        size_of::<CHeader>(),
        Classification::TargetConditioned,
        "derived from repr(C) plus the current target ABI",
    ),
    obs("DocumentId size", size_of::<DocumentId>(), Classification::Guaranteed, "repr(transparent) follows u64 layout"),
    obs("String owner size", size_of::<String>(), Classification::Observed, "does not include buffer capacity"),
    obs("String payload bytes", text.len(), Classification::Guaranteed, "UTF-8 byte length"),
    obs("Vec owner size", size_of::<Vec<u32>>(), Classification::Observed, "does not include allocation"),
    obs(
        "boxed slice owner size",
        size_of::<Box<[u32]>>(),
        Classification::TargetConditioned,
        "metadata-bearing owner whose concrete width is target-conditioned",
    ),
    obs("boxed slice payload", size_of_val(&*boxed), Classification::Guaranteed, "element count times u32 size"),
    obs(
        "Rc<str> owner size",
        size_of::<Rc<str>>(),
        Classification::TargetConditioned,
        "metadata-bearing shared owner whose concrete width is target-conditioned",
    ),
    obs("Rc<str> payload", size_of_val(&*shared), Classification::Guaranteed, "UTF-8 byte length"),
    obs("marker size", size_of::<Marker>(), Classification::Guaranteed, "empty marker is zero-sized"),
    obs(
        "slice-reference size",
        size_of::<&[u8]>(),
        Classification::TargetConditioned,
        "wide reference shape is semantic; concrete byte width depends on the target",
    ),
    ]
}
fn obs(name: &'static str, value: usize, classification: Classification, note: &'static str) -> Observation {
    Observation {
        name, value, classification, note
    }
}
pub fn expected_c_header_size() -> usize {
    let mut offset = 0;
    offset = align_up(offset, align_of::<u8>()) + size_of::<u8>();
    offset = align_up(offset, align_of::<u32>()) + size_of::<u32>();
    offset = align_up(offset, align_of::<u16>()) + size_of::<u16>();
    align_up(offset, align_of::<CHeader>())
}
fn align_up(value: usize, alignment: usize) -> usize {
    let remainder = value % alignment;
    if remainder == 0 {
        value
    }
    else {
        value + alignment - remainder
    }
}
pub fn target_description() -> String {
    format!("{}-{}", std::env::consts::ARCH, std::env::consts::OS)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn repr_c_calculation_matches_current_target() {
        assert_eq!(size_of::<CHeader>(), expected_c_header_size());
    }
    #[test]
    fn transparent_layout_matches_field() {
        assert_eq!(size_of::<DocumentId>(), size_of::<u64>());
        assert_eq!(align_of::<DocumentId>(), align_of::<u64>());
    }
    #[test]
    fn documented_pointer_niche_relationship() {
        assert_eq!(size_of::<Option<&u8>>(), size_of::<&u8>());
    }
    #[test]
    fn report_labels_observations() {
        let rows = report();
        assert!(rows.iter().any(|row| {
            row.name == "String owner size"
                && row.classification == Classification::Observed
        }));
        assert!(!target_description().is_empty());
    }
}
