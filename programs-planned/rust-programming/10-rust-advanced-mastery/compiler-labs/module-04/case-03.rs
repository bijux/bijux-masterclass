struct I<const N:usize>(usize);impl<const N:usize>I<N>{fn new(v:usize)->Option<Self>{(v<N).then_some(Self(v))}fn get(self)->usize{self.0}}fn main(){assert_eq!(I::<2>::new(1).map(I::get),Some(1));}
