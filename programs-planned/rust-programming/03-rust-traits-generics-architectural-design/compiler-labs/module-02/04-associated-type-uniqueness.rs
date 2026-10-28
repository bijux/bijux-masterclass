trait Source{type Item;}struct S;impl Source for S{type Item=u8;}impl Source for S{type Item=u16;}fn main(){}
