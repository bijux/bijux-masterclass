trait Label{fn label(&self)->&str;}
fn show<T>(value:&T){println!("{}",value.label());}
fn main(){}
