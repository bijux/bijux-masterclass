#[derive(Debug,PartialEq)] enum Action{Write{path:String,text:String}}
fn plan(name:&str)->Vec<Action>{vec![Action::Write{path:format!("{name}.txt"),text:name.to_owned()}]}
fn main(){assert_eq!(plan("a").len(),1);}
