class Token { #value = 1; static isToken(value: unknown): value is Token { return typeof value === 'object' && value !== null && #value in value; } read(): number { return this.#value; } }
const value: unknown = new Token();
if (Token.isToken(value)) console.log(value.read());
