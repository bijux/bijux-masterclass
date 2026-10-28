use rust_foundations_lab_10_inventory_ledger::{Command, ItemState, Ledger, execute};

#[test]
fn public_session_preserves_variant_specific_borrower() {
    let mut ledger = Ledger::new();
    execute(&mut ledger, Command::Add(String::from("caliper"))).expect("add");
    let id = ledger.items()[0].id();
    execute(
        &mut ledger,
        Command::Checkout {
            id,
            borrower: String::from("Ada"),
        },
    )
    .expect("checkout");
    assert_eq!(
        ledger.find(id).map(|item| item.state()),
        Some(&ItemState::CheckedOut {
            borrower: String::from("Ada"),
        })
    );
    let output = execute(&mut ledger, Command::List(None)).expect("list");
    assert_eq!(output.output(), "1 [checked-out: Ada] caliper");
}

#[test]
fn failed_transition_does_not_claim_change() {
    let mut ledger = Ledger::new();
    let id = ledger.add(String::from("caliper")).expect("add");
    let before = ledger.clone();
    assert!(execute(&mut ledger, Command::Return(id)).is_err());
    assert_eq!(ledger, before);
}
