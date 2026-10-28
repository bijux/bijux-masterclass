use course5_metacases_macros::require_public; #[require_public] pub fn answer()->u32{42} fn main(){assert_eq!(answer(),42);}
