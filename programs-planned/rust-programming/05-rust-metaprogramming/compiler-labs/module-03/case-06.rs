macro_rules! states { ($name:ident; $($state:ident),+) => { enum $name { $($state),+ } }; }
states!(State; Draft, Draft);
fn main(){}
