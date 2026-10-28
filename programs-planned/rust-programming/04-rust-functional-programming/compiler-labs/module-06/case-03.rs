struct Bag(Vec<i32>);
impl<'a> IntoIterator for &'a Bag {
    type Item=&'a i32; type IntoIter=std::slice::Iter<'a,i32>;
    fn into_iter(self)->Self::IntoIter { self.0.iter() }
}
fn main(){ let bag=Bag(vec![1,2]); assert_eq!((&bag).into_iter().sum::<i32>(),3); }
