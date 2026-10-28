struct Bad;
impl Iterator for Bad {
    type Item = &'static str;
    fn next(&mut self) -> Option<Self::Item> {
        let text = String::from("temporary");
        Some(text.as_str())
    }
}
fn main() {}
