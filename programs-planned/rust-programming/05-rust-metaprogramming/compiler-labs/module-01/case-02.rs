macro_rules! marker { ($name:ident) => { #[derive(Debug)] struct $name; }; }
marker!(Ready);
fn main() { let _ = Ready; }
