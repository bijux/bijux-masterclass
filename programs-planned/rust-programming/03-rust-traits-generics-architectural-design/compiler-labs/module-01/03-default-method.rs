trait Named{fn name(&self)->&str;fn greeting(&self)->String{format!("hello {}",self.name())}}
struct User;impl Named for User{fn name(&self)->&str{"Ada"}}
fn main(){assert_eq!(User.greeting(),"hello Ada");}
