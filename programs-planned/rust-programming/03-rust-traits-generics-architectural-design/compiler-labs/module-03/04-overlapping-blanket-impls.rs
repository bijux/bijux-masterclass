trait Mark{}trait A{}trait B{}impl<T:A> Mark for T{}impl<T:B> Mark for T{}fn main(){}
