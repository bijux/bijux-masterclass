fn assert_send<T:Send>(){}fn main(){assert_send::<Vec<u8>>();}
