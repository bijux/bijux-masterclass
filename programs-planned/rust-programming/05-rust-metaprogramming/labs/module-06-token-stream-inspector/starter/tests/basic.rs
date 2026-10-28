use c5_lab06_token_inspector_starter::token_tree_shape;

#[test]
fn baseline_expands_to_a_string_literal() {
    assert_eq!(token_tree_shape!(alpha), "uninspected");
}
