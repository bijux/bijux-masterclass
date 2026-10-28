struct I<const N:usize>(usize);impl<const N:usize>I<N>{fn new(v:usize)->Option<Self>{(v<N).then_some(Self(v))}}fn main(){let i=I::<4>::new(3).unwrap();assert_eq!(i.0,3);}
