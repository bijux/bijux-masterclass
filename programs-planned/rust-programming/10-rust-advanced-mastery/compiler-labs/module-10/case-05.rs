enum V{One,Two}fn read(v:V)->u8{match v{V::One=>1,V::Two=>2}}fn main(){assert_eq!(read(V::One),1);assert_eq!(read(V::Two),2);}
