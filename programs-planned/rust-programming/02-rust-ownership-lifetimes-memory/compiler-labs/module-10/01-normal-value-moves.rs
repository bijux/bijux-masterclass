// outcome: pass
// lesson: Ordinary values remain movable

struct T(String);fn main(){let a=T("x".into());let b=a;assert_eq!(b.0,"x");}
