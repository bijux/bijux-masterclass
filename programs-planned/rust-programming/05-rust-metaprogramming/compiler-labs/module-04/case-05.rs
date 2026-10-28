macro_rules! once {($e:expr)=>{{let __macro_value=$e;__macro_value+__macro_value}};}
fn main(){let __macro_value=99;assert_eq!(once!(3),6);assert_eq!(__macro_value,99);}
