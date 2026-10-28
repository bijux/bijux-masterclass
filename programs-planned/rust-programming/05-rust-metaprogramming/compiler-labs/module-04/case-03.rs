fn handler(x:u32)->u32{x+1}
macro_rules! call {($path:path,$arg:expr)=>{$path($arg)};}
fn main(){assert_eq!(call!(handler,4),5);}
