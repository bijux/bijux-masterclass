fn main() {
    let numbers = vec![1, 2].into_iter();
    let words = vec!["a", "b"].into_iter();
    let _combined = numbers.chain(words);
}
