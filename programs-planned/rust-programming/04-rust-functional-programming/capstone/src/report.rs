use crate::analysis::Analysis;
use crate::diagnostic::Severity;
use crate::domain::AccountId;
use crate::ledger::AccountStatus;
use crate::query::{account_timeline, events_for_account};

pub fn render_diagnostics(analysis: &Analysis) -> String {
    analysis
        .diagnostics()
        .iter()
        .map(ToString::to_string)
        .collect::<Vec<_>>()
        .join("\n")
}

pub fn render_summary(analysis: &Analysis) -> String {
    let open_accounts = analysis
        .ledger()
        .accounts()
        .values()
        .filter(|state| state.status() == AccountStatus::Open)
        .count();
    let closed_accounts = analysis.ledger().accounts().len() - open_accounts;
    let total_balance: i128 = analysis
        .ledger()
        .accounts()
        .values()
        .map(|state| i128::from(state.balance()))
        .sum();

    [
        "LEDGERFLOW SUMMARY".to_owned(),
        format!("rows_inspected\t{}", analysis.inspected_rows()),
        format!("events_accepted\t{}", analysis.accepted().len()),
        format!("diagnostics\t{}", analysis.diagnostics().len()),
        format!("errors\t{}", analysis.error_count()),
        format!("warnings\t{}", analysis.warning_count()),
        format!("accounts\t{}", analysis.ledger().accounts().len()),
        format!("open_accounts\t{open_accounts}"),
        format!("closed_accounts\t{closed_accounts}"),
        format!("total_balance_cents\t{total_balance}"),
    ]
    .join("\n")
}

pub fn render_accounts(analysis: &Analysis) -> String {
    analysis
        .ledger()
        .accounts()
        .iter()
        .map(|(id, state)| {
            format!(
                "ACCOUNT\t{}\t{}\t{}\t{}",
                id,
                state.status().as_str(),
                state.balance(),
                state.accepted_events()
            )
        })
        .collect::<Vec<_>>()
        .join("\n")
}

pub fn render_account(analysis: &Analysis, account: &AccountId) -> Option<String> {
    let state = analysis.ledger().get(account)?;
    let mut lines = vec![format!(
        "ACCOUNT\t{}\t{}\t{}\t{}",
        account,
        state.status().as_str(),
        state.balance(),
        state.accepted_events()
    )];
    for point in account_timeline(analysis, account) {
        match point {
            Ok(point) => lines.push(format!(
                "EVENT\t{}\t{}\t{}\t{}\t{}",
                point.event().line(),
                point.event().id(),
                point.event().kind(),
                point.event().amount(),
                point.balance_after()
            )),
            Err(_) => lines.push("QUERY_ERROR\ttimeline arithmetic overflow".to_owned()),
        }
    }
    Some(lines.join("\n"))
}

fn render_event(event: &crate::domain::Event) -> String {
    format!(
        "EVENT\t{}\t{}\t{}\t{}\t{}\t{}",
        event.line(),
        event.id(),
        event.account(),
        event.kind(),
        event.amount(),
        event.note().unwrap_or("")
    )
}

pub fn render_events(analysis: &Analysis, account: Option<&AccountId>) -> String {
    match account {
        Some(id) => events_for_account(analysis, id)
            .map(render_event)
            .collect::<Vec<_>>()
            .join("\n"),
        None => analysis
            .accepted()
            .iter()
            .map(render_event)
            .collect::<Vec<_>>()
            .join("\n"),
    }
}

pub fn render_check(analysis: &Analysis) -> String {
    let diagnostics = render_diagnostics(analysis);
    let summary = render_summary(analysis);
    if diagnostics.is_empty() {
        summary
    } else {
        format!("{diagnostics}\n{summary}")
    }
}

pub fn warning_codes(analysis: &Analysis) -> impl Iterator<Item = &'static str> + '_ {
    analysis
        .diagnostics()
        .iter()
        .filter(|item| item.severity() == Severity::Warning)
        .map(|item| item.code())
}

#[cfg(test)]
mod tests {
    use super::{render_accounts, render_check, render_summary};
    use crate::analysis::analyze;

    #[test]
    fn account_rendering_is_lexically_deterministic() {
        let analysis = analyze(concat!(
            "LEDGERFLOW-V1\n",
            "1\tz\topen\t0\tz\n",
            "2\ta\topen\t0\ta\n",
        ));
        let rendered = render_accounts(&analysis);
        assert!(rendered.starts_with("ACCOUNT\ta\t"));
    }

    #[test]
    fn repeated_rendering_is_identical() {
        let analysis = analyze("LEDGERFLOW-V1\n1\ta\topen\t0\tstart\n");
        assert_eq!(render_summary(&analysis), render_summary(&analysis));
        assert_eq!(render_check(&analysis), render_check(&analysis));
    }
}
