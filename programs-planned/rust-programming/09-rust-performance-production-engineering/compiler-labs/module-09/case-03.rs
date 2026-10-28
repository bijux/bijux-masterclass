#[derive(PartialEq, Eq, PartialOrd, Ord)]
struct Product(&'static str, &'static str);

impl Product {
    fn architecture(&self) -> &'static str {
        self.0
    }

    fn profile(&self) -> &'static str {
        self.1
    }
}

fn main() {
    let expected = Product("x86_64", "dist");
    let supported = [Product("x86_64", "dist")];
    assert!(supported.contains(&expected));
    assert_eq!(expected.architecture(), "x86_64");
    assert_eq!(expected.profile(), "dist");
}
