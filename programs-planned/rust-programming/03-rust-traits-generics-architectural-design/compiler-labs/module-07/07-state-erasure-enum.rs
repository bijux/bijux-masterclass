struct D;struct R;struct X<S>(S);enum Any{D(X<D>),R(X<R>)}fn main(){let a=Any::D(X(D));match a{Any::D(_)=>{},Any::R(_)=>{}}let _=Any::R(X(R));}
