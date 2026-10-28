struct Token;
macro_rules! duplicate {($value:expr)=>{{fn need<T:Clone>(v:T)->(T,T){(v.clone(),v)}need($value)}};}
fn main(){let _=duplicate!(Token);}
