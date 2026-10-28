fn use_it<T:Clone>(_:T){}struct NotClone;fn main(){use_it(NotClone);}
