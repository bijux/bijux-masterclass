fn main() { let data = String::from("large"); let view = &data[..]; drop(data); println!("{view}"); }
