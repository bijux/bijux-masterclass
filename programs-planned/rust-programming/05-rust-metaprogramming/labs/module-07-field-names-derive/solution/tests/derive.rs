#![allow(dead_code)]

use c5_lab07_field_names_solution::FieldNames;

struct Opaque;

#[derive(FieldNames)]
struct User<T, const N: usize>
where
    T: Clone,
{
    id: u64,
    #[field_names(rename = "display-name")]
    name: String,
    #[field_names(skip)]
    cache: [T; N],
    opaque: Opaque,
}

#[derive(FieldNames)]
struct Marker;

#[test]
fn names_follow_policy_without_new_type_bounds() {
    assert_eq!(
        User::<String, 2>::FIELD_NAMES,
        &["id", "display-name", "opaque"],
    );
    assert_eq!(User::<String, 2>::FIELD_COUNT, 3);
}

#[test]
fn a_unit_struct_has_no_fields() {
    assert!(Marker::FIELD_NAMES.is_empty());
}
