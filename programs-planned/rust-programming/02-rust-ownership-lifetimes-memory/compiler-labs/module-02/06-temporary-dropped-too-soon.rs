// outcome: fail
// lesson: A method borrow cannot outlive a temporary owner statement

fn make()->String{String::from("x")} fn main(){let view=make().as_str(); println!("{view}");}
