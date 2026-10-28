fn main() {
    let _ = [1, -1].into_iter().fold(0, |sum, value| {
        if value > 0 { sum + value } else { None }
    });
}
