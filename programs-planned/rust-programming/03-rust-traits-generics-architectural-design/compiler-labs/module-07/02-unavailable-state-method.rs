struct Draft;struct Reviewed;struct Doc<S>(S);impl Doc<Reviewed>{fn publish(self){}}fn main(){Doc(Draft).publish();}
