fn main() {
    let mut values = vec![1, 2];
    let mut first = values.iter_mut();
    let mut second = values.iter_mut();
    println!("{:?} {:?}", first.next(), second.next());
}
