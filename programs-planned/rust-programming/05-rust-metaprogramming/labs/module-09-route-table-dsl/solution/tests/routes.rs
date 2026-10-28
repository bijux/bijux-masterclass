use c5_lab09_route_solution::route_table;

fn list(_input: &str) -> String {
    "list".to_owned()
}

fn create(input: &str) -> String {
    format!("create:{input}")
}

route_table! {
    pub static ROUTES {
        GET "/users" => list;
        POST "/users" => create;
    }
}

#[test]
fn order_and_dispatch_are_deterministic() {
    assert_eq!(ROUTES.len(), 2);
    assert_eq!(ROUTES[0].path, "/users");
    assert_eq!(
        dispatch(Method::Post, "/users", "x"),
        Some("create:x".to_owned()),
    );
    assert_eq!(dispatch(Method::Delete, "/users", "x"), None);
}
