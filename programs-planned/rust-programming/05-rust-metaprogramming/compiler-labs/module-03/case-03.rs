macro_rules! pairs { (@parse [$($out:expr,)*]) => {[$($out,)*]}; (@parse [$($out:expr,)*] $a:literal=>$b:literal; $($rest:tt)*) => {pairs!(@parse [$($out,)* ($a,$b),] $($rest)*)}; ($($input:tt)*) => {pairs!(@parse [] $($input)*)}; }
fn main(){assert_eq!(pairs!("a"=>1;"b"=>2;).len(),2);}
