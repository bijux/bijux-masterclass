// outcome: fail
// lesson: Annotations cannot make a local owner survive return

fn bad<'a>()->&'a str{let value=String::from("gone"); value.as_str()} fn main(){}
