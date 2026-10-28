export interface ChildCommand {
    readonly program: string;
    readonly args: readonly string[];
}
export function validateCommand(command: ChildCommand): void { if (command.program.length === 0)
    throw new Error('program is required'); if (command.args.some(a => a.includes('\0')))
    throw new Error('arguments cannot contain NUL'); }
