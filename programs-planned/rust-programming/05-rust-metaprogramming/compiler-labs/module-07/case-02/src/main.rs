use course5_metacases_macros::TypeName; #[derive(TypeName)] enum Mode{A,B} fn main(){assert_eq!(Mode::TYPE_NAME,"Mode");}
