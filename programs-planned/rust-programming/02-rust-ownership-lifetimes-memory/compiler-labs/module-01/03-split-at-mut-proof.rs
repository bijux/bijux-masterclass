// outcome: pass
// lesson: split_at_mut returns nonoverlapping slices
fn main() {
    let mut values=[1,2];
    let (left,right)=values.split_at_mut(1);
    left[0]+=right[0];
    assert_eq!(values,[3,2]);
}
