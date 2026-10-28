use std::time::Duration;

pub async fn process(values: Vec<u64>) -> Vec<u64> {
    let mut output = Vec::with_capacity(values.len());
    for value in values {
        tokio::time::sleep(Duration::from_millis(1)).await;
        output.push(value * 2);
    }
    output
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn preserves_source_order() {
        assert_eq!(process(vec![3, 1, 2]).await, vec![6, 2, 4]);
    }
}
