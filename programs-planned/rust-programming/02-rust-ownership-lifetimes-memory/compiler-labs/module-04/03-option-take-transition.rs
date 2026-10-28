// outcome: pass
// lesson: Option::take leaves a valid represented state
struct G{
    value:Option<String>
}
impl Drop for G{
    fn drop(&mut self){
        let _=self.value.take();
    }
}
fn main(){
    let mut g=G{
        value:Some("x".into())
    };
    let v=g.value.take();
    assert_eq!(v.as_deref(),Some("x"));
}
