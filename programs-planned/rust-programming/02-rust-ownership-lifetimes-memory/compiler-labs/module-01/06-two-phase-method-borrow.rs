// outcome: pass
// lesson: Method receiver reservation permits vec.push(vec.len())

fn main(){let mut values=vec![10]; values.push(values.len()); assert_eq!(values,[10,1]);}
