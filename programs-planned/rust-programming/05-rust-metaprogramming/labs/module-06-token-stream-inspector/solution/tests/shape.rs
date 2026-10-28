use c5_lab06_token_inspector_solution::{
    token_tree_shape, top_level_token_count,
};

#[test]
fn nested_groups_are_structural() {
    let shape = token_tree_shape!(alpha + (beta * 3));
    assert!(shape.contains("Ident(alpha)"));
    assert!(shape.contains("Group(Paren:["));
}

#[test]
fn joint_punctuation_is_visible() {
    let shape = token_tree_shape!(a::b => c);
    assert!(shape.contains("Punct(:,Joint)"));
    assert!(shape.contains("Punct(=,Joint)"));
}

#[test]
fn a_group_is_one_top_level_token_tree() {
    assert_eq!(top_level_token_count!((a + b)), 1);
}
