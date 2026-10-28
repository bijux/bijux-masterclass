macro_rules! sum { (@go $acc:expr;) => {$acc}; (@go $acc:expr; $next:literal $(, $rest:literal)*) => {sum!(@go $acc+$next; $($rest),*)}; ($($n:literal),*) => {sum!(@go 0; $($n),*)}; }
fn main(){let _=sum!(1, two, 3);}
