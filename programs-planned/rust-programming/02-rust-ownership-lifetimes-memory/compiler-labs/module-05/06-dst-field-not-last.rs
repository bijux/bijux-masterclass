// outcome: fail
// lesson: A dynamically sized field must be last

struct Bad<T:?Sized>{tail:T,after:u8}fn main(){}
