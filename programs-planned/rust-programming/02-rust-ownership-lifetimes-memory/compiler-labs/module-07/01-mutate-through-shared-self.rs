// outcome: fail
// lesson: Ordinary field mutation requires exclusive receiver

struct C{n:u64}impl C{fn inc(&self){self.n+=1;}}fn main(){}
