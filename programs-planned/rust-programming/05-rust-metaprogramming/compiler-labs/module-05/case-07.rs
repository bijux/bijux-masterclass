macro_rules! names {($($n:ident),+)=>{&[$(stringify!($n)),+]};}
fn main(){assert_eq!(names!(First,Second), &["First","Second"]);}
