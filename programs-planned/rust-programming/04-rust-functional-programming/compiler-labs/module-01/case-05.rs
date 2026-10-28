fn twice<F>(mut function: F) where F: FnMut() { function(); function(); }
fn main() {
    let mut calls = 0;
    twice(|| calls += 1);
    assert_eq!(calls, 2);
}
