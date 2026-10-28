fn main() { let mut data = vec![1,2,3]; let view = &data[..]; data.push(4); println!("{view:?}"); }
