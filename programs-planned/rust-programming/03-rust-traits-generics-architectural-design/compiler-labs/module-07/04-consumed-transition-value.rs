struct D;struct R;struct X<S>(S);impl X<D>{fn go(self)->X<R>{X(R)}}fn main(){let x=X(D);let _y=x.go();let _z=x;}
