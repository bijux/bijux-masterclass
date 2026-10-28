fn normalize(s:&str)->String{s.split_whitespace().collect::<Vec<_>>().join(" ").to_lowercase()}
fn main(){for s in [""," A ","a  b"]{let once=normalize(s);assert_eq!(normalize(&once),once);}}
