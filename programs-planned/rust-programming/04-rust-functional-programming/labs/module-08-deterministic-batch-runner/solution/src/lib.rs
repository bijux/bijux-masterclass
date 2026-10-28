#![forbid(unsafe_code)]

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Input {
    pub name: String,
    pub due: u64,
    pub valid: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Scheduled {
    pub id: u64,
    pub name: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Action {
    Write { path: String, contents: String },
    Notify { message: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Analysis {
    pub scheduled: Vec<Scheduled>,
    pub rejected: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Plan {
    pub analysis: Analysis,
    pub actions: Vec<Action>,
}

pub fn plan<I, F>(inputs: I, now: u64, mut next_id: F) -> Plan
where
    I: IntoIterator<Item = Input>,
    F: FnMut() -> u64,
{
    let mut analysis = Analysis::default();
    let mut actions = Vec::new();

    for input in inputs {
        if !input.valid {
            analysis.rejected.push(format!("{}: invalid", input.name));
            continue;
        }
        if input.due < now {
            analysis.rejected.push(format!("{}: overdue", input.name));
            continue;
        }
        let id = next_id();
        analysis.scheduled.push(Scheduled {
            id,
            name: input.name.clone(),
        });
        actions.push(Action::Write {
            path: format!("jobs/{id}.txt"),
            contents: input.name,
        });
    }

    Plan { analysis, actions }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExecutionFailure<E> {
    pub completed: usize,
    pub source: E,
}

pub fn execute<E, F>(
    actions: &[Action],
    mut perform: F,
) -> Result<usize, ExecutionFailure<E>>
where
    F: FnMut(&Action) -> Result<(), E>,
{
    let mut completed = 0;
    for action in actions {
        if let Err(source) = perform(action) {
            return Err(ExecutionFailure { completed, source });
        }
        completed += 1;
    }
    Ok(completed)
}

pub fn render_dry_run(plan: &Plan) -> String {
    plan.actions
        .iter()
        .enumerate()
        .map(|(index, action)| match action {
            Action::Write { path, contents } => format!(
                "{}\tWRITE\t{}\t{} bytes",
                index + 1,
                path,
                contents.len()
            ),
            Action::Notify { message } => {
                format!("{}\tNOTIFY\t{}", index + 1, message)
            }
        })
        .collect::<Vec<_>>()
        .join("\n")
}

#[cfg(test)]
mod tests {
    use super::{Action, ExecutionFailure, Input, execute, plan, render_dry_run};
    use std::cell::Cell;

    #[test]
    fn rejected_inputs_do_not_consume_ids() {
        let next = Cell::new(10);
        let output = plan(
            [
                Input {
                    name: "bad".to_owned(),
                    due: 10,
                    valid: false,
                },
                Input {
                    name: "ok".to_owned(),
                    due: 10,
                    valid: true,
                },
            ],
            5,
            || {
                let value = next.get();
                next.set(value + 1);
                value
            },
        );
        assert_eq!(output.analysis.scheduled[0].id, 10);
        assert_eq!(next.get(), 11);
    }

    #[test]
    fn execution_reports_the_successful_prefix() {
        let output = plan(
            [
                Input {
                    name: "a".to_owned(),
                    due: 10,
                    valid: true,
                },
                Input {
                    name: "b".to_owned(),
                    due: 10,
                    valid: true,
                },
            ],
            0,
            {
                let mut id = 0;
                move || {
                    id += 1;
                    id
                }
            },
        );
        let mut calls = 0;
        let result = execute(&output.actions, |_| {
            calls += 1;
            if calls == 2 { Err("stop") } else { Ok(()) }
        });
        assert_eq!(
            result,
            Err(ExecutionFailure {
                completed: 1,
                source: "stop",
            })
        );
    }

    #[test]
    fn dry_run_is_a_value_transformation_not_execution() {
        let output = plan(
            [Input {
                name: "a".to_owned(),
                due: 1,
                valid: true,
            }],
            0,
            || 1,
        );
        let rendered = render_dry_run(&output);
        assert_eq!(rendered, "1\tWRITE\tjobs/1.txt\t1 bytes");
        assert!(matches!(output.actions[0], Action::Write { .. }));
    }
}
