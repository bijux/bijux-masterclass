fn main() {
    let values = vec![1, 2, 3];
    let _owned: Vec<_> = values.into_iter().collect();
    println!("{}", values.len());
}
