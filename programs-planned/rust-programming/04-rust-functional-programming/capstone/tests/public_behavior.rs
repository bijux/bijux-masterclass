use ledgerflow::{AccountId, DiagnosticKind, Severity, analyze};
use ledgerflow::query::{account_timeline, diagnostics_with_severity};

#[test]
fn complete_valid_stream_has_deterministic_state_and_audit() {
    let input = concat!(
        "LEDGERFLOW-V1\n",
        "1\tb\topen\t0\tb\n",
        "2\ta\topen\t0\ta\n",
        "3\ta\tdeposit\t10\tfund\n",
        "4\ta\twithdraw\t10\tspend\n",
        "5\ta\tclose\t0\tdone\n",
    );
    let analysis = analyze(input);
    assert!(!analysis.has_errors());
    assert_eq!(analysis.accepted().len(), 5);
    assert_eq!(analysis.audit().len(), 5);
    let account = AccountId::parse("a").unwrap();
    let balances: Vec<_> = account_timeline(&analysis, &account)
        .map(|point| point.unwrap().balance_after())
        .collect();
    assert_eq!(balances, vec![0, 10, 0, 0]);
    let ids: Vec<_> = analysis
        .ledger()
        .accounts()
        .keys()
        .map(AccountId::as_str)
        .collect();
    assert_eq!(ids, vec!["a", "b"]);
}

#[test]
fn warnings_and_errors_remain_separate_channels() {
    let input = concat!(
        "LEDGERFLOW-V1\n",
        " 1 \t a \t open \t 0 \t start \n",
        "2\ta\twithdraw\t1\tbad\n",
    );
    let analysis = analyze(input);
    assert!(analysis.has_errors());
    assert_eq!(
        diagnostics_with_severity(&analysis, Severity::Warning).count(),
        5
    );
    assert_eq!(
        diagnostics_with_severity(&analysis, Severity::Error).count(),
        1
    );
    assert!(matches!(
        analysis.diagnostics().last().unwrap().kind(),
        DiagnosticKind::InsufficientFunds { .. }
    ));
}
