use course5_metacases_macros::TypeName; struct NotClone; #[derive(TypeName)] struct Wrap<T> where T: Clone { value:T } fn main(){let _=Wrap{value:NotClone};}
