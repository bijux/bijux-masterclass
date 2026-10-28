fn allocate<F:FnMut()->u64>(count:usize,mut next:F)->Vec<u64>{(0..count).map(|_|next()).collect()}
fn main(){let mut n=0;assert_eq!(allocate(3,||{n+=1;n}),vec![1,2,3]);}
