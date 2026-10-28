// Predict before compiling.
fn sum_three(values: [i32; 3]) -> i32 {
    values.into_iter().sum()
}

fn main() {
    println!("{}", sum_three([1, 2, 3, 4]));
}
