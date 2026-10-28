//! Contract harness for the independent inventory-ledger assessment.
//!
//! No domain representation is supplied: selecting the model is part of the
//! transfer proof. The stable help contract lets the package execute before the
//! learner adds commands and persistence.

/// Supported starter contract identifier.
pub const CONTRACT_VERSION: &str = "INVENTORY-LEDGER-LAB-V1";

/// Command surface the finished product must support.
pub const HELP: &str = concat!(
    "inventory-ledger add <name...>\n",
    "inventory-ledger list [available|checked-out|retired]\n",
    "inventory-ledger checkout <id> <borrower...>\n",
    "inventory-ledger return <id>\n",
    "inventory-ledger retire <id>\n",
    "inventory-ledger search <query...>\n",
    "inventory-ledger stats\n",
    "inventory-ledger help\n",
);

/// Renders the stable starter help surface.
pub const fn help() -> &'static str {
    HELP
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn baseline_exposes_the_full_command_contract() {
        for command in [
            "add",
            "list",
            "checkout",
            "return",
            "retire",
            "search",
            "stats",
            "help",
        ] {
            assert!(HELP.contains(command));
        }
        assert_eq!(CONTRACT_VERSION, "INVENTORY-LEDGER-LAB-V1");
    }
}
