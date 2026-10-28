fn count_valid(input:&str)->usize{input.lines().filter(|line|!line.trim().is_empty()).count()}
fn main(){assert_eq!(count_valid("a\n\nb\n"),2);}
