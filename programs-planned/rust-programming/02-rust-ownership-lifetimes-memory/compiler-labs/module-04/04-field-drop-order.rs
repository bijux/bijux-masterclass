// outcome: pass
// lesson: A trace can observe deterministic field order
struct T(&'static str);
impl Drop for T{
    fn drop(&mut self){
        print!("{}",self.0);
    }
}
struct S{
    a:T,b:T
}
fn main(){
    let _s=S{
        a:T("a"),b:T("b")
    };
}
