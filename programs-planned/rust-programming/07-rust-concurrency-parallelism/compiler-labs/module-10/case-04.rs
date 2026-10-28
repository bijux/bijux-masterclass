fn main(){ let sizes=[3usize,4,5]; let total=sizes.into_iter().try_fold(0usize,usize::checked_add); assert_eq!(total,Some(12)); }
