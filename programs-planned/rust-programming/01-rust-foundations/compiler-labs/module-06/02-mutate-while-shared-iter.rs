// Predict before compiling.
fn main() {
    let mut values = vec![1, 2];
    let mut iter = values.iter();
    values.push(3);
    println!("{:?}", iter.next());
}
