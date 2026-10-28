export interface FileEntry { readonly name: string; readonly size: number }
export function renderEntries(entries: readonly FileEntry[]): string {
  return entries.map((entry) => `${entry.name}\t${entry.size}`).join('\n') + (entries.length === 0 ? '' : '\n');
}
