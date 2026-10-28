// Predict before compiling.
fn ids(flag: bool) -> impl Iterator<Item = u64> {
    if flag { [1, 2].into_iter() } else { std::iter::once(3) }
}
fn main() { println!("{}", ids(true).count()); }
