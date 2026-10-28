use course5_metacases_macros::TypeName; #[derive(TypeName)] struct Generic<T>(T); fn main(){assert_eq!(Generic::<u8>::TYPE_NAME,"Generic");}
