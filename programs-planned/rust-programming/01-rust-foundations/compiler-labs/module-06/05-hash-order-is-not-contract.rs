// Predict before compiling.
use std::collections::HashMap;
fn main() {
    let counts = HashMap::from([("todo", 2), ("done", 1), ("doing", 3)]);
    let rendered = counts.into_iter().map(|(k,v)| format!("{k}:{v}")).collect::<Vec<_>>().join(",");
    assert_eq!(rendered, "todo:2,doing:3,done:1");
}
