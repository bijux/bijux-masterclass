use course5_metacases_macros::TypeName; #[derive(TypeName)] struct Wrap<T> where T: Clone { value:T } fn main(){assert_eq!(Wrap::<String>::TYPE_NAME,"Wrap");}
