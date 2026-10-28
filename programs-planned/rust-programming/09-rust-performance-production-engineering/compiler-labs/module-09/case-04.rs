fn size_change(old:u64,new:u64)->Option<i128>{Some(i128::from(new)-i128::from(old))} fn main(){assert_eq!(size_change(100,80),Some(-20));}
