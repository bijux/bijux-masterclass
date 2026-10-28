fn main() {
    let _values: Vec<i32> = ["1", "2"].into_iter().map(str::parse::<i32>).collect();
}
