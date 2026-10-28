fn checked(x:u8)->Result<u8,&'static str>{if x<3{Ok(x)}else{Err("large")}}fn main(){assert!(checked(4).is_err());}
