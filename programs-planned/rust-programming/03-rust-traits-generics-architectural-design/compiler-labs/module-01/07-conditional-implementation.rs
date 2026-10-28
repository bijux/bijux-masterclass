trait Render{fn render(&self)->String;} impl Render for u8{fn render(&self)->String{self.to_string()}}
struct Wrapped<T>(T);impl<T:Render> Render for Wrapped<T>{fn render(&self)->String{format!("[{}]",self.0.render())}}
fn main(){assert_eq!(Wrapped(3).render(),"[3]");}
