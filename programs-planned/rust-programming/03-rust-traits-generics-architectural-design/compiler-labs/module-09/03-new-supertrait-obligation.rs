trait Id{fn id(&self)->u8;}trait P:Id{fn run(&self){}}struct Old;impl P for Old{}fn main(){}
