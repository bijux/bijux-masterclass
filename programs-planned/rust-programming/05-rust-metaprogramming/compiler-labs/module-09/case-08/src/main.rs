use course5_metacases_macros::unique_idents; fn main(){let n=unique_idents!(get,post).iter().filter(|s|s.len()>3).count();assert_eq!(n,1);}
