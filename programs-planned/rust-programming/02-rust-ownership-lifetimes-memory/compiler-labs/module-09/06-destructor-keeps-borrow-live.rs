// outcome: fail
// lesson: Drop can be the final use of a borrowed field
struct I<'a>(&'a str);
impl Drop for I<'_>{
    fn drop(&mut self){
        println!("{}",self.0);
    }
}
fn main(){
    let i;
    {
        let s=String::from("x");
        i=I(&s);
    }
    drop(i);
}
