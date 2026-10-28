macro_rules! named {($name:ident)=>{stringify!($name)};($($bad:tt)*)=>{compile_error!("expected one identifier")};}
fn main(){assert_eq!(named!(alpha),"alpha");}
