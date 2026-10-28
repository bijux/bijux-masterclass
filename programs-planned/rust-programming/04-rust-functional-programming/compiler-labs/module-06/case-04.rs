struct Bag(Vec<i32>);
impl<'a> IntoIterator for &'a Bag {
    type Item=&'a i32; type IntoIter=std::slice::Iter<'a,i32>;
    fn into_iter(self)->Self::IntoIter { self.0.iter() }
}
impl<'a> IntoIterator for &'a Bag {
    type Item=&'a i32; type IntoIter=std::slice::Iter<'a,i32>;
    fn into_iter(self)->Self::IntoIter { self.0.iter() }
}
fn main() {}
