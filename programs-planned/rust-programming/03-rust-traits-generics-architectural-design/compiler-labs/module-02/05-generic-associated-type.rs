trait View{type Out<'a> where Self:'a;fn view(&self)->Self::Out<'_>;}struct Text(String);
impl View for Text{type Out<'a>=&'a str where Self:'a;fn view(&self)->&str{&self.0}}
fn main(){let t=Text("x".into());assert_eq!(t.view(),"x");}
