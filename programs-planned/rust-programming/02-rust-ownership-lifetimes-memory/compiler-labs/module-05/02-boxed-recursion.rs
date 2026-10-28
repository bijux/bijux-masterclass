// outcome: pass
// lesson: Box gives recursive edges fixed size

enum List{End,Next(Box<List>)}fn main(){let _=List::Next(Box::new(List::End));}
