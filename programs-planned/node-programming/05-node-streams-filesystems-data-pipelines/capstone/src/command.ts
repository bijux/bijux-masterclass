import { UsageError } from './errors.js';
export type Command = {
    readonly kind: 'inspect';
    readonly input: string;
    readonly gzipInput: boolean;
} | {
    readonly kind: 'normalize';
    readonly input: string;
    readonly output: string;
    readonly gzipInput: boolean;
    readonly gzipOutput: boolean;
    readonly replace: boolean;
} | {
    readonly kind: 'filter';
    readonly input: string;
    readonly output: string;
    readonly selectedKind: string;
    readonly gzipInput: boolean;
    readonly gzipOutput: boolean;
    readonly replace: boolean;
} | {
    readonly kind: 'verify';
    readonly input: string;
    readonly sha256: string;
} | {
    readonly kind: 'through';
    readonly input: string;
    readonly output: string;
    readonly program: string;
    readonly args: readonly string[];
    readonly replace: boolean;
} | {
    readonly kind: 'help';
} | {
    readonly kind: 'version';
};
function takeFlag(args: string[], name: string): boolean { const i = args.indexOf(name); if (i < 0)
    return false; args.splice(i, 1); return true; }
function takeValue(args: string[], name: string): string | undefined { const i = args.indexOf(name); if (i < 0)
    return undefined; const value = args[i + 1]; if (value === undefined)
    throw new UsageError(`${name} requires a value`); args.splice(i, 2); return value; }
function noExtras(args: readonly string[]): void { if (args.length > 0)
    throw new UsageError(`unexpected arguments: ${args.join(' ')}`); }
export function parseCommand(argv: readonly string[]): Command {
    const [name, ...rest] = argv;
    if (!name || name === 'help' || name === '--help')
        return { kind: 'help' };
    if (name === 'version' || name === '--version')
        return { kind: 'version' };
    if (name === 'inspect') {
        const args = [...rest];
        const gzipInput = takeFlag(args, '--gzip-input');
        const input = args.shift();
        if (!input)
            throw new UsageError('inspect requires <input>');
        noExtras(args);
        return { kind: 'inspect', input, gzipInput };
    }
    if (name === 'normalize') {
        const args = [...rest];
        const gzipInput = takeFlag(args, '--gzip-input'), gzipOutput = takeFlag(args, '--gzip-output'), replace = takeFlag(args, '--replace');
        const input = args.shift(), output = args.shift();
        if (!input || !output)
            throw new UsageError('normalize requires <input> <output>');
        noExtras(args);
        return { kind: 'normalize', input, output, gzipInput, gzipOutput, replace };
    }
    if (name === 'filter') {
        const args = [...rest];
        const gzipInput = takeFlag(args, '--gzip-input'), gzipOutput = takeFlag(args, '--gzip-output'), replace = takeFlag(args, '--replace');
        const selectedKind = takeValue(args, '--kind');
        const input = args.shift(), output = args.shift();
        if (!input || !output || !selectedKind)
            throw new UsageError('filter requires <input> <output> --kind <kind>');
        noExtras(args);
        return { kind: 'filter', input, output, selectedKind, gzipInput, gzipOutput, replace };
    }
    if (name === 'verify') {
        const args = [...rest];
        const sha256 = takeValue(args, '--sha256');
        const input = args.shift();
        if (!input || !sha256)
            throw new UsageError('verify requires <input> --sha256 <hex>');
        if (!/^[0-9a-fA-F]{64}$/u.test(sha256))
            throw new UsageError('sha256 must contain 64 hexadecimal characters');
        noExtras(args);
        return { kind: 'verify', input, sha256: sha256.toLowerCase() };
    }
    if (name === 'through') {
        const args = [...rest];
        const split = args.indexOf('--');
        if (split < 0)
            throw new UsageError('through requires -- before program');
        const before = args.slice(0, split), after = args.slice(split + 1);
        const replace = takeFlag(before, '--replace');
        const input = before.shift(), output = before.shift(), program = after.shift();
        if (!input || !output || !program)
            throw new UsageError('through requires <input> <output> -- <program> [args...]');
        noExtras(before);
        return { kind: 'through', input, output, program, args: after, replace };
    }
    throw new UsageError(`unknown command: ${name}`);
}
