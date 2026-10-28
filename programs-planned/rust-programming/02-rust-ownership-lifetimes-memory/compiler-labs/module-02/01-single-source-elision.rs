// outcome: pass
// lesson: One input reference determines output

fn trim(s:&str)->&str{s.trim()} fn main(){let s=String::from(" x "); assert_eq!(trim(&s),"x");}
