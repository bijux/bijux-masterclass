fn twice<F>(function: F) where F: Fn() { function(); function(); }
fn main() {
    let mut calls = 0;
    twice(|| calls += 1);
}
