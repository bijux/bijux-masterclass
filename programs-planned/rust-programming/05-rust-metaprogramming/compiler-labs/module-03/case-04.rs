macro_rules! transition { ($a:ident => $b:ident;) => {()}; ($a:ident $b:ident;) => {compile_error!("expected `=>` between states")}; }
fn main(){transition!(Draft Review);}
