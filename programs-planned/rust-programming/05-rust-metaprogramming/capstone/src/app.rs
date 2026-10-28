use crate::exit_codes::{EXIT_COMMAND_FAILURE, EXIT_SUCCESS, EXIT_USAGE_FAILURE};
use crate::{find_command, AppError, CommandSpec, COMMANDS};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Execution {
    pub output: String,
    pub exit_code: i32,
}

impl Execution {
    fn success(output: String) -> Self { Self { output, exit_code: EXIT_SUCCESS } }
}

pub fn help_text() -> String {
    [
        "CommandForge — compile-time validated command catalog",
        "",
        "USAGE:",
        "  commandforge list",
        "  commandforge explain <command>",
        "  commandforge run <command> [command arguments]",
        "  commandforge demo",
        "  commandforge help",
        "  commandforge version",
    ].join("\n")
}

fn render_descriptor(command: &CommandSpec) -> String {
    let descriptor = &command.handler;
    let usage = if descriptor.usage.is_empty() {
        command.name.to_owned()
    } else {
        format!("{} {}", command.name, descriptor.usage)
    };
    let mut lines = vec![
        format!("NAME: {}", command.name),
        format!("ABOUT: {}", descriptor.about),
        format!("USAGE: commandforge run {usage}"),
    ];
    if !descriptor.arguments.is_empty() {
        lines.push("ARGUMENTS:".to_owned());
        for argument in descriptor.arguments {
            let requirement = if argument.required { "required" } else { "optional" };
            lines.push(format!("  {:<14} {:<8} {}", argument.flag, requirement, argument.help));
        }
    }
    lines.join("\n")
}

pub fn execute(arguments: &[String]) -> Result<Execution, AppError> {
    let Some(command) = arguments.first().map(String::as_str) else {
        return Err(AppError::Usage(help_text()));
    };

    match command {
        "list" => {
            if arguments.len() != 1 {
                return Err(AppError::Usage("`list` accepts no arguments".to_owned()));
            }
            let output = COMMANDS
                .iter()
                .map(|command| format!("{:<10} {}", command.name, command.handler.about))
                .collect::<Vec<_>>()
                .join("\n");
            Ok(Execution::success(output))
        }
        "explain" => {
            if arguments.len() != 2 {
                return Err(AppError::Usage("usage: commandforge explain <command>".to_owned()));
            }
            let command = find_command(&arguments[1])
                .ok_or_else(|| AppError::UnknownCommand(arguments[1].clone()))?;
            Ok(Execution::success(render_descriptor(command)))
        }
        "run" => {
            let Some(name) = arguments.get(1) else {
                return Err(AppError::Usage(
                    "usage: commandforge run <command> [command arguments]".to_owned(),
                ));
            };
            let command = find_command(name)
                .ok_or_else(|| AppError::UnknownCommand(name.clone()))?;
            let output = (command.handler.invoke)(&arguments[2..]).map_err(AppError::Command)?;
            Ok(Execution::success(output))
        }
        "demo" => {
            if arguments.len() != 1 {
                return Err(AppError::Usage("`demo` accepts no arguments".to_owned()));
            }
            let scenarios = [
                vec!["run", "add", "--left", "7", "--right", "35"],
                vec!["run", "slug", "--text", "Compile Time Architecture"],
                vec!["run", "repeat", "--text", "ha", "--times", "3"],
                vec!["run", "contains", "--text", "metaprogramming", "--needle", "gram"],
            ];
            let mut output = Vec::new();
            for scenario in scenarios {
                let owned = scenario.into_iter().map(str::to_owned).collect::<Vec<_>>();
                let result = execute(&owned)?;
                output.push(format!("$ commandforge {}\n{}", owned.join(" "), result.output));
            }
            Ok(Execution::success(output.join("\n\n")))
        }
        "help" | "--help" | "-h" => Ok(Execution::success(help_text())),
        "version" | "--version" | "-V" => Ok(Execution::success(format!(
            "commandforge {}",
            env!("CARGO_PKG_VERSION")
        ))),
        other => Err(AppError::UnknownCommand(other.to_owned())),
    }
}

pub fn exit_code_for_error(error: &AppError) -> i32 {
    match error {
        AppError::Usage(_) | AppError::UnknownCommand(_) => EXIT_USAGE_FAILURE,
        AppError::Command(_) => EXIT_COMMAND_FAILURE,
    }
}
