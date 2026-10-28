struct Diagnostics(Vec<String>);
impl FromIterator<String> for Diagnostics {
    fn from_iter<I:IntoIterator<Item=String>>(iter:I)->Self { Self(iter.into_iter().collect()) }
}
fn main(){ let _d:Diagnostics=["a"].into_iter().collect(); }
