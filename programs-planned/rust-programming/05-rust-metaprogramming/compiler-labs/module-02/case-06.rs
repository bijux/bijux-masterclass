macro_rules! count { ($( $item:expr ),+ $(,)?) => { <[()]>::len(&[$({ let _=&$item; () }),+]) }; }
fn main() { assert_eq!(count!(10,20,30,),3); }
