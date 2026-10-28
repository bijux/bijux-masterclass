// outcome: fail
// lesson: A field cannot be moved out of a Drop type directly
struct G{
    value:String
}
impl Drop for G{
    fn drop(&mut self){
        println!("{}",self.value);
    }
}
fn main(){
    let g=G{
        value:"x".into()
    };
    let _v=g.value;
}
