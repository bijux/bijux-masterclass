use std::ops::ControlFlow;
fn main() {
    let result = [2, 4, 8].into_iter().try_fold(0, |sum, value| {
        let next = sum + value;
        if next > 5 { ControlFlow::Break(next) } else { ControlFlow::Continue(next) }
    });
    assert_eq!(result, ControlFlow::Break(6));
}
