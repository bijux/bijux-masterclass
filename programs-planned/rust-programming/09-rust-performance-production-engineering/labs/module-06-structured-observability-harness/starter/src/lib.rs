#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Event {
    pub name: &'static str,
    pub message: String,
}

pub fn accepted(request_id: u64) -> Event {
    Event { name: "accepted", message: format!("accepted request {request_id}") }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn creates_an_event() {
        assert_eq!(accepted(7).name, "accepted");
    }
}
