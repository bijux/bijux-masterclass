#[repr(C)]struct Pair{a:u8,b:u32}fn main(){let pair=Pair{a:1,b:2};assert_eq!(u32::from(pair.a)+pair.b,3);assert!(std::mem::size_of::<Pair>()>=5);}
