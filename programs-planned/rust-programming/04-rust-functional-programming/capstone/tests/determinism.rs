use ledgerflow::analyze;
use ledgerflow::report::{render_accounts, render_check, render_events, render_summary};

#[test]
fn all_public_reports_are_repeatable_for_the_same_value() {
    let input = concat!(
        "LEDGERFLOW-V1\n",
        "1\tz\topen\t0\tz\n",
        "2\ta\topen\t0\ta\n",
        "3\ta\tdeposit\t4\tfund\n",
    );
    let analysis = analyze(input);
    for render in [
        render_summary as fn(&ledgerflow::Analysis) -> String,
        render_accounts,
        render_check,
    ] {
        assert_eq!(render(&analysis), render(&analysis));
    }
    assert_eq!(
        render_events(&analysis, None),
        render_events(&analysis, None)
    );
}
