#[derive(Default)] struct Diagnostics(Vec<String>);
impl Extend<String> for Diagnostics {
    fn extend<I:IntoIterator<Item=String>>(&mut self,iter:I){self.0.extend(iter);}
}
fn main(){let mut d=Diagnostics::default();d.extend(["a".to_owned()]);assert_eq!(d.0.len(),1);}
