fn main() {
    let values = [1, 2, 3];
    let _prefix: Vec<_> = values
        .iter()
        .take_while(|value: &i32| *value < 3)
        .collect();
}
