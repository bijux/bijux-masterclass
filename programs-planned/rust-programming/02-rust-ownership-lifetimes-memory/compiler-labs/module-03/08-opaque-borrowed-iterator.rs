// outcome: pass
// lesson: An opaque iterator captures the receiver borrow
struct C{
    v:Vec<String>
}
impl C{
    fn items(&self)->impl Iterator<Item=&str>+'_ {
        self.v.iter().map(String::as_str)
    }
}
fn main(){
    let c=C{
        v:vec!["x".into()]
    };
    assert_eq!(c.items().next(),Some("x"));
}
