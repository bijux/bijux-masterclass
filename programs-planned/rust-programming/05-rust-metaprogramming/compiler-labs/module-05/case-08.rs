macro_rules! names {($($n:ident),+)=>{&[$(stringify!($n)),+]};}
fn main(){let _=names!(First;Second);}
