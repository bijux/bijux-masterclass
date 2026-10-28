use commandforge_macros::command_catalog;

command_catalog! {
    pub static COMMANDS;
    pub fn find_command;
    {
        "add" => crate::handlers::ADD_HANDLER;
        "slug" => crate::handlers::SLUG_HANDLER;
        "repeat" => crate::handlers::REPEAT_HANDLER;
        "contains" => crate::handlers::CONTAINS_HANDLER;
    }
}
