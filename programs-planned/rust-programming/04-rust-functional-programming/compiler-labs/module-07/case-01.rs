enum List { End, Link(i32, Box<List>) }
fn main(){ let _list=List::Link(1,Box::new(List::End)); }
