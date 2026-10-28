// Predict before compiling.
fn main() {
    let numbers = (1_u64, 2_u64);
    let numbers_copy = numbers;
    println!("{numbers:?} {numbers_copy:?}");

    let owned = (1_u64, String::from("two"));
    let moved = owned;
    println!("{owned:?} {moved:?}");
}
