enum V{A(u8),B(u8)}fn value(v:V)->u8{match v{V::A(x)|V::B(x)=>x}}fn main(){assert_eq!(value(V::A(1))+value(V::B(2)),3);}
