trait Api{fn existing(&self);fn added(&self);}struct S;impl Api for S{fn existing(&self){}}fn main(){}
