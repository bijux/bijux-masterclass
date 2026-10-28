struct Draft;struct Reviewed;struct Doc<S>(S);impl Doc<Draft>{fn review(self)->Doc<Reviewed>{Doc(Reviewed)}}fn main(){let _:Doc<Reviewed>=Doc(Draft).review();}
