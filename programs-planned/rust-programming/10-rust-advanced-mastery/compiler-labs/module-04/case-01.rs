fn same<const N:usize>(a:[u8;N])->[u8;N]{a}fn main(){assert_eq!(same([1,2]),[1,2]);}
