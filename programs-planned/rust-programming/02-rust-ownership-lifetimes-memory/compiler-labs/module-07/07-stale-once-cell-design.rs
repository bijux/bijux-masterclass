// outcome: pass
// lesson: A one-time cache can compile despite mutable source
use std::cell::OnceCell;
struct D{
    text:String,len:OnceCell<usize>
}
impl D{
    fn len(&self)->usize{
        *self.len.get_or_init(||self.text.len())
    }
    fn change(&mut self){
        self.text.push('x');
    }
}
fn main(){
    let mut d=D{
        text:"a".into(),len:OnceCell::new()
    };
    assert_eq!(d.len(),1);
    d.change();
    assert_eq!(d.len(),1);
}
