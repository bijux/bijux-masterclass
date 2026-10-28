fn main() {
    let total = [1_u8, 2].into_iter().map(u16::from).sum();
    println!("{total:?}");
}
