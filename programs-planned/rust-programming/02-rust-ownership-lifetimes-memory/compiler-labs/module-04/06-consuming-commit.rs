// outcome: pass
// lesson: Commit consumes the session
struct E{
    working:Option<String>
}
impl E{
    fn commit(mut self)->String{
        match self.working.take(){
            Some(v)=>v,None=>String::new()
        }
    }
}
fn main(){
    let e=E{
        working:Some("x".into())
    };
    assert_eq!(e.commit(),"x");
}
