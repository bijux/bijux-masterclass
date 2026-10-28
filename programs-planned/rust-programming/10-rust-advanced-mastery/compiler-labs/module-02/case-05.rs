#[derive(Debug,PartialEq)]enum E<A,B>{A(A),B(B)}fn main(){let a:E<&str,u8>=E::A("bad");let b:E<&str,u8>=E::B(7);assert_eq!(a,E::A("bad"));assert_eq!(b,E::B(7));}
