fn main(){let x=7;let p=&x as *const i32;let y=unsafe{*p};assert_eq!(y,7);}
