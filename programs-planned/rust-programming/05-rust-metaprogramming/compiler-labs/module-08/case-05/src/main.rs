use course5_metacases_macros::metadata; #[metadata(add)] fn answer()->u32{42} fn main(){assert_eq!((ADD_METADATA.1)(),42);}
