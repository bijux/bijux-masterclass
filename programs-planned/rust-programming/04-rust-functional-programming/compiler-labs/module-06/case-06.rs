struct Diagnostics(Vec<String>);
impl FromIterator<String> for Diagnostics {
    fn from_iter<I:IntoIterator<Item=String>>(iter:I)->Self { Self(iter.into_iter().collect()) }
}
fn main(){ let d:Diagnostics=["a".to_owned()].into_iter().collect(); assert_eq!(d.0.len(),1); }
