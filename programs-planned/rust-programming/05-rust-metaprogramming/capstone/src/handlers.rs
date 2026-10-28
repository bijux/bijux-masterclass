use crate::CommandError;
use commandforge_macros::{command_handler, CommandArgs};

#[derive(Debug, CommandArgs)]
pub struct AddArgs {
    #[arg(help = "left signed integer")]
    pub left: i64,
    #[arg(help = "right signed integer")]
    pub right: i64,
}

#[command_handler(about = "Add two signed integers with overflow checking")]
pub fn add(arguments: AddArgs) -> Result<String, CommandError> {
    arguments
        .left
        .checked_add(arguments.right)
        .map(|value| value.to_string())
        .ok_or_else(|| CommandError::Domain("signed integer addition overflowed".to_owned()))
}

#[derive(Debug, CommandArgs)]
pub struct SlugArgs {
    #[arg(help = "text to normalize")]
    pub text: String,
}

#[command_handler(about = "Normalize text into a lowercase ASCII slug")]
pub fn slug(arguments: SlugArgs) -> Result<String, CommandError> {
    let mut output = String::new();
    let mut pending_separator = false;
    for character in arguments.text.chars() {
        if character.is_ascii_alphanumeric() {
            if pending_separator && !output.is_empty() {
                output.push('-');
            }
            output.push(character.to_ascii_lowercase());
            pending_separator = false;
        } else if !output.is_empty() {
            pending_separator = true;
        }
    }
    if output.is_empty() {
        return Err(CommandError::Domain(
            "slug input must contain at least one ASCII letter or digit".to_owned(),
        ));
    }
    Ok(output)
}

#[derive(Debug, CommandArgs)]
pub struct RepeatArgs {
    #[arg(help = "text to repeat")]
    pub text: String,
    #[arg(default = "1", help = "number of repetitions from 1 through 20")]
    pub times: u32,
}

#[command_handler(about = "Repeat text a bounded number of times")]
pub fn repeat(arguments: RepeatArgs) -> Result<String, CommandError> {
    if !(1..=20).contains(&arguments.times) {
        return Err(CommandError::Domain(
            "`--times` must be between 1 and 20".to_owned(),
        ));
    }
    Ok(arguments.text.repeat(arguments.times as usize))
}

#[derive(Debug, CommandArgs)]
pub struct ContainsArgs {
    #[arg(help = "text to search")]
    pub text: String,
    #[arg(help = "substring to locate")]
    pub needle: String,
}

#[command_handler(about = "Test whether text contains a substring")]
pub fn contains(arguments: ContainsArgs) -> Result<String, CommandError> {
    Ok(arguments.text.contains(&arguments.needle).to_string())
}
