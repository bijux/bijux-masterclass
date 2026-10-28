fn twice<F:Fn()>(f:F){f();f();}fn main(){let mut n=0;twice(||n+=1);}
