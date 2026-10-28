enum C{Add(u8),Clear}fn run(c:C)->u8{match c{C::Add(x)=>x,C::Clear=>0}}fn main(){assert_eq!(run(C::Add(2)),2);let _=C::Clear;}
