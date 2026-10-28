#![allow(dead_code)]
trait Component { type Error; fn name(&self) -> &'static str; }
struct Tcp;
impl Component for Tcp { type Error = std::io::Error; fn name(&self) -> &'static str { "tcp" } }
fn main() { let component = Tcp; assert_eq!(component.name(), "tcp"); }
