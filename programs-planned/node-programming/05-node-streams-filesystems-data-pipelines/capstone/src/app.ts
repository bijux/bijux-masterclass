import { throughChild } from './child.js';
import type { Command } from './command.js';
import { inspectFile, transformFile, verifyFile } from './pipeline.js';
import { HELP, render } from './render.js';

export const VERSION = '1.0.0';

export async function execute(
  command: Command,
  signal?: AbortSignal,
): Promise<string> {
  switch (command.kind) {
    case 'help':
      return HELP;
    case 'version':
      return `flowledger ${VERSION}\n`;
    case 'inspect':
      return render(await inspectFile(command.input, command.gzipInput, signal));
    case 'normalize':
      return render(
        await transformFile(command.input, command.output, {
          gzipInput: command.gzipInput,
          gzipOutput: command.gzipOutput,
          replace: command.replace,
          signal,
        }),
      );
    case 'filter':
      return render(
        await transformFile(command.input, command.output, {
          kind: command.selectedKind,
          gzipInput: command.gzipInput,
          gzipOutput: command.gzipOutput,
          replace: command.replace,
          signal,
        }),
      );
    case 'verify':
      return render(await verifyFile(command.input, command.sha256, signal));
    case 'through':
      return render(
        await throughChild(
          command.input,
          command.output,
          command.program,
          command.args,
          command.replace,
          signal,
        ),
      );
  }
}
