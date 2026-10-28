use course5_metacases_macros::unique_idents; fn main(){let v:&[&str]=unique_idents!();assert!(v.is_empty());}
