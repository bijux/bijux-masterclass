fn main() {
    let mut values = vec![1];
    let length = || values.len();
    values.push(2);
    println!("{}", length());
}
