use course5_metacases_macros::FieldCount; struct NoDisplay; #[derive(FieldCount)] struct Record<T>{a:T,b:NoDisplay} fn main(){assert_eq!(Record::<u8>::FIELD_COUNT,2);}
