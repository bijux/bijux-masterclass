fn main() {
    let left = vec![1, 2];
    let right = vec![3, 4];
    let _pairs: Vec<_> = left.into_iter().zip(right).collect();
    println!("{}", left.len());
}
