struct Once(Option<i32>);
impl Iterator for Once { type Item=i32; fn next(&mut self)->Option<i32>{self.0.take()} }
impl std::iter::FusedIterator for Once {}
fn main(){ let mut it=Once(Some(1)); assert_eq!(it.next(),Some(1)); assert_eq!(it.next(),None); }
