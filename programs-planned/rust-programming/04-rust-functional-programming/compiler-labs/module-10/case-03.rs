fn parse(lines:&[&str])->Result<Vec<i64>,std::num::ParseIntError>{lines.iter().map(|s|s.parse()).collect()}
fn main(){assert_eq!(parse(&["1","2"]).unwrap(),vec![1,2]);}
