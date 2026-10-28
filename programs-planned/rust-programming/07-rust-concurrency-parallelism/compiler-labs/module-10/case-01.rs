fn main(){ let mut slots=[None,None]; for (i,v) in [(1,20),(0,10)]{slots[i]=Some(v);} assert_eq!(slots,[Some(10),Some(20)]); }
