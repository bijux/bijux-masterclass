use crate::analysis::analyze;
use crate::domain::AccountId;
use crate::report::{render_account, render_accounts, render_check, render_events, render_summary};
use std::path::{Path, PathBuf};

pub const EXIT_OK: u8 = 0;
pub const EXIT_DATA_ERROR: u8 = 1;
pub const EXIT_COMMAND_ERROR: u8 = 2;
/// Compatibility name for the command-error exit class.
pub const EXIT_USAGE: u8 = EXIT_COMMAND_ERROR;

pub const DEMO_SOURCE: &str = concat!(
    "LEDGERFLOW-V1\n",
    "1\tacct-a\topen\t0\tprimary account\n",
    "2\tacct-a\tdeposit\t5000\tfunds\n",
    "3\tacct-a\twithdraw\t5000\tsettlement\n",
    "4\tacct-a\tclose\t0\tcomplete\n",
    "5\tacct-b\topen\t0\tsecondary\n",
    "6\tacct-b\twithdraw\t1\trejected: no funds\n",
);

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    Check { path: PathBuf },
    Summary { path: PathBuf },
    Account { path: PathBuf, account: AccountId },
    Events { path: PathBuf, account: Option<AccountId> },
    Demo,
    Help,
    Version,
}

impl Command {
    pub fn path(&self) -> Option<&Path> {
        match self {
            Self::Check { path }
            | Self::Summary { path }
            | Self::Account { path, .. }
            | Self::Events { path, .. } => Some(path),
            Self::Demo | Self::Help | Self::Version => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UsageError {
    message: String,
}

impl UsageError {
    pub fn message(&self) -> &str {
        &self.message
    }
}

fn usage_error(message: impl Into<String>) -> UsageError {
    UsageError {
        message: message.into(),
    }
}

pub fn help_text() -> &'static str {
    concat!(
        "LedgerFlow — deterministic ledger-event analysis\n\n",
        "USAGE\n",
        "  ledgerflow check <events.tsv>\n",
        "  ledgerflow summary <events.tsv>\n",
        "  ledgerflow account <events.tsv> <account-id>\n",
        "  ledgerflow events <events.tsv> [account-id]\n",
        "  ledgerflow demo\n",
        "  ledgerflow help\n",
        "  ledgerflow version\n"
    )
}

pub fn parse_args<I, S>(args: I) -> Result<Command, UsageError>
where
    I: IntoIterator<Item = S>,
    S: Into<String>,
{
    let args: Vec<String> = args.into_iter().map(Into::into).collect();
    let Some(command) = args.first().map(String::as_str) else {
        return Ok(Command::Help);
    };

    match (command, &args[1..]) {
        ("check", [path]) => Ok(Command::Check {
            path: PathBuf::from(path.as_str()),
        }),
        ("summary", [path]) => Ok(Command::Summary {
            path: PathBuf::from(path.as_str()),
        }),
        ("account", [path, account]) => Ok(Command::Account {
            path: PathBuf::from(path.as_str()),
            account: AccountId::parse(account)
                .map_err(|_| usage_error(format!("invalid account id {account:?}")))?,
        }),
        ("events", [path]) => Ok(Command::Events {
            path: PathBuf::from(path.as_str()),
            account: None,
        }),
        ("events", [path, account]) => Ok(Command::Events {
            path: PathBuf::from(path.as_str()),
            account: Some(
                AccountId::parse(account)
                    .map_err(|_| usage_error(format!("invalid account id {account:?}")))?,
            ),
        }),
        ("demo", []) => Ok(Command::Demo),
        ("help" | "--help" | "-h", []) => Ok(Command::Help),
        ("version" | "--version" | "-V", []) => Ok(Command::Version),
        _ => Err(usage_error(format!(
            "invalid command or arguments\n\n{}",
            help_text()
        ))),
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AppOutcome {
    stdout: String,
    stderr: String,
    exit_code: u8,
}

impl AppOutcome {
    pub fn success(stdout: impl Into<String>) -> Self {
        Self {
            stdout: stdout.into(),
            stderr: String::new(),
            exit_code: EXIT_OK,
        }
    }

    pub fn failure(stderr: impl Into<String>) -> Self {
        Self {
            stdout: String::new(),
            stderr: stderr.into(),
            exit_code: EXIT_COMMAND_ERROR,
        }
    }

    pub fn stdout(&self) -> &str {
        &self.stdout
    }

    pub fn stderr(&self) -> &str {
        &self.stderr
    }

    pub fn exit_code(&self) -> u8 {
        self.exit_code
    }
}

pub fn execute_text(command: &Command, input: &str) -> AppOutcome {
    match command {
        Command::Help => AppOutcome::success(help_text()),
        Command::Version => AppOutcome::success(concat!("ledgerflow ", env!("CARGO_PKG_VERSION"))),
        Command::Demo => execute_text(
            &Command::Summary {
                path: PathBuf::from("<demo>"),
            },
            DEMO_SOURCE,
        ),
        Command::Check { .. } => from_analysis(input, render_check),
        Command::Summary { .. } => from_analysis(input, |analysis| {
            let accounts = render_accounts(analysis);
            if accounts.is_empty() {
                render_summary(analysis)
            } else {
                format!("{}\n{}", render_summary(analysis), accounts)
            }
        }),
        Command::Account { account, .. } => {
            let analysis = analyze(input);
            match render_account(&analysis, account) {
                Some(rendered) => AppOutcome {
                    stdout: rendered,
                    stderr: String::new(),
                    exit_code: if analysis.has_errors() {
                        EXIT_DATA_ERROR
                    } else {
                        EXIT_OK
                    },
                },
                None => AppOutcome::failure(format!("account {account} was not found")),
            }
        }
        Command::Events { account, .. } => from_analysis(input, |analysis| {
            render_events(analysis, account.as_ref())
        }),
    }
}

fn from_analysis<F>(input: &str, render: F) -> AppOutcome
where
    F: FnOnce(&crate::Analysis) -> String,
{
    let analysis = analyze(input);
    AppOutcome {
        stdout: render(&analysis),
        stderr: String::new(),
        exit_code: if analysis.has_errors() {
            EXIT_DATA_ERROR
        } else {
            EXIT_OK
        },
    }
}

#[cfg(test)]
mod tests {
    use super::{Command, EXIT_DATA_ERROR, EXIT_OK, EXIT_USAGE, execute_text, parse_args};

    #[test]
    fn argument_parser_rejects_shape_errors() {
        let error = parse_args(["account", "file.tsv"]).unwrap_err();
        assert!(error.message().contains("invalid command"));
    }

    #[test]
    fn check_distinguishes_data_errors_from_usage_errors() {
        let command = Command::Check {
            path: "x".into(),
        };
        assert_eq!(
            execute_text(&command, "LEDGERFLOW-V1\n1\ta\topen\t0\tx\n").exit_code(),
            EXIT_OK
        );
        assert_eq!(
            execute_text(&command, "LEDGERFLOW-V1\n1\ta\twithdraw\t1\tx\n").exit_code(),
            EXIT_DATA_ERROR
        );
        let missing = parse_args(["unknown"]).unwrap_err();
        assert!(missing.message().contains("USAGE"));
        assert_eq!(EXIT_USAGE, 2);
    }
}
