// outcome: fail
// lesson: A view into mutably borrowed scratch cannot escape the method
struct S{
    buf:String
}
impl S{
    fn load(&mut self,input:&str)->&str{
        self.buf.clear();
        self.buf.push_str(input);
        &self.buf
    }
}
fn main(){
    let view;
    let mut s=S{
        buf:String::new()
    };
    view=s.load("a");
    s.load("b");
    println!("{view}");
}
