fn main() {
    let _values: Vec<i32> = ["1", "2"]
        .into_iter()
        .map(|text| text.parse::<i32>()?)
        .collect();
}
