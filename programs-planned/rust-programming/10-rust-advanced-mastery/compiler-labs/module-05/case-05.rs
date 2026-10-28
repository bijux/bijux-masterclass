use std::any::Any;fn main(){let x:Box<dyn Any>=Box::new(7_u8);assert_eq!(x.downcast_ref::<u8>(),Some(&7));}
