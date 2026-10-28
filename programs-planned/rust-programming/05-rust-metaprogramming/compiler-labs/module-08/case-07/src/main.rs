use course5_metacases_macros::require_public; #[require_public] #[inline] pub fn plus(a:u32,b:u32)->u32{a+b} fn main(){assert_eq!(plus(2,3),5);}
