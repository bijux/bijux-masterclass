trait Finish{fn finish(self)->usize;} impl Finish for String{fn finish(self)->usize{self.len()}}
fn main(){let s=String::from("x");let _=s.finish();println!("{s}");}
