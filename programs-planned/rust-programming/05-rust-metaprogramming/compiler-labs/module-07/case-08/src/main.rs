use course5_metacases_macros::FieldCount; #[derive(FieldCount)] struct Marker; fn main(){assert_eq!(Marker::FIELD_COUNT,0);}
