struct Empty;struct Ready;struct B<S>(S);impl B<Empty>{fn ready(self)->B<Ready>{B(Ready)}}impl B<Ready>{fn build(self){}}fn main(){B(Empty).build();}
