use c5_lab07_field_names_starter::FieldNames;

#[derive(FieldNames)]
struct Empty;

#[test]
fn baseline_preserves_the_derived_type() {
    assert!(Empty::FIELD_NAMES.is_empty());
}
