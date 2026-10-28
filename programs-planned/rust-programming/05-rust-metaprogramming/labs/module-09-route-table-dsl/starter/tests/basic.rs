use c5_lab09_route_starter::route_table;

route_table! {}

#[test]
fn baseline_generates_an_item() {
    assert_eq!(ROUTE_COUNT, 0);
}
