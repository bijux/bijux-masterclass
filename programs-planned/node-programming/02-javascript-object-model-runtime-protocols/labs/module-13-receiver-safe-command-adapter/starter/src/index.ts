export type Command<Args extends readonly unknown[], Result> = (...args: Args) => Result;
export class CommandRegistry {
  readonly #commands = new Map<string, Command<readonly unknown[], unknown>>();
  register(name: string, command: Command<readonly unknown[], unknown>): void {
    if (this.#commands.has(name)) throw new Error(`duplicate command: ${name}`);
    this.#commands.set(name, command);
  }
  names(): readonly string[] { return [...this.#commands.keys()].sort(); }
}
