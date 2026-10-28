use std::collections::BTreeMap; fn main() { let fields = BTreeMap::from([("operation","ingest"),("outcome","ok")]); assert_eq!(fields.len(), 2); }
