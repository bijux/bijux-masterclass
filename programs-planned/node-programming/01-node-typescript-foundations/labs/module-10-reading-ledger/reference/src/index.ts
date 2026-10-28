import { readFile, rename, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';

interface BaseBook { readonly id: number; readonly title: string; readonly addedAt: string }
export interface QueuedBook extends BaseBook { readonly state: 'queued' }
export interface ReadingBook extends BaseBook { readonly state: 'reading'; readonly startedAt: string }
export interface FinishedBook extends BaseBook { readonly state: 'finished'; readonly startedAt: string; readonly finishedAt: string; readonly pages: number }
export interface DroppedBook extends BaseBook { readonly state: 'dropped'; readonly droppedAt: string; readonly reason: string }
export type Book = QueuedBook | ReadingBook | FinishedBook | DroppedBook;
export interface ReadingLedger { readonly nextId: number; readonly books: readonly Book[] }

export function emptyLedger(): ReadingLedger { return { nextId: 1, books: [] }; }
export function addBook(ledger: ReadingLedger, rawTitle: string, addedAt: string): ReadingLedger {
  const title = rawTitle.trim();
  if (title === '') throw new Error('title must not be empty');
  const book: QueuedBook = { state: 'queued', id: ledger.nextId, title, addedAt };
  return { nextId: ledger.nextId + 1, books: [...ledger.books, book] };
}
function replace(ledger: ReadingLedger, id: number, change: (book: Book) => Book): ReadingLedger {
  let found = false;
  const books = ledger.books.map((book) => book.id === id ? (found = true, change(book)) : book);
  if (!found) throw new Error(`missing book ${id}`);
  return { ...ledger, books };
}
export function startBook(ledger: ReadingLedger, id: number, startedAt: string): ReadingLedger {
  return replace(ledger, id, (book) => {
    if (book.state !== 'queued') throw new Error(`cannot start ${book.state} book`);
    return { ...book, state: 'reading', startedAt };
  });
}
export function finishBook(ledger: ReadingLedger, id: number, pages: number, finishedAt: string): ReadingLedger {
  if (!Number.isSafeInteger(pages) || pages <= 0) throw new Error('pages must be a positive safe integer');
  return replace(ledger, id, (book) => {
    if (book.state !== 'reading') throw new Error(`cannot finish ${book.state} book`);
    return { ...book, state: 'finished', pages, finishedAt };
  });
}
export function encodeLedger(ledger: ReadingLedger): string {
  return JSON.stringify({ format: 'READING_LEDGER_V1', nextId: ledger.nextId, books: [...ledger.books].sort((a,b) => a.id-b.id) }, null, 2) + '\n';
}
function isRecord(value: unknown): value is Record<string, unknown> { return typeof value === 'object' && value !== null && !Array.isArray(value); }
export function decodeLedger(text: string): ReadingLedger {
  const value: unknown = JSON.parse(text);
  if (!isRecord(value) || value['format'] !== 'READING_LEDGER_V1' || !Number.isSafeInteger(value['nextId']) || !Array.isArray(value['books'])) {
    throw new Error('invalid reading ledger header');
  }
  const books: Book[] = value['books'].map((raw, index) => {
    if (!isRecord(raw) || !Number.isSafeInteger(raw['id']) || typeof raw['title'] !== 'string' || typeof raw['addedAt'] !== 'string' || typeof raw['state'] !== 'string') {
      throw new Error(`invalid book at index ${index}`);
    }
    const base = { id: raw['id'] as number, title: raw['title'], addedAt: raw['addedAt'] };
    switch (raw['state']) {
      case 'queued': return { ...base, state: 'queued' };
      case 'reading': if (typeof raw['startedAt'] === 'string') return { ...base, state: 'reading', startedAt: raw['startedAt'] }; break;
      case 'finished': if (typeof raw['startedAt'] === 'string' && typeof raw['finishedAt'] === 'string' && Number.isSafeInteger(raw['pages']) && (raw['pages'] as number) > 0) return { ...base, state: 'finished', startedAt: raw['startedAt'], finishedAt: raw['finishedAt'], pages: raw['pages'] as number }; break;
      case 'dropped': if (typeof raw['droppedAt'] === 'string' && typeof raw['reason'] === 'string') return { ...base, state: 'dropped', droppedAt: raw['droppedAt'], reason: raw['reason'] }; break;
    }
    throw new Error(`invalid ${String(raw['state'])} book at index ${index}`);
  });
  return { nextId: value['nextId'] as number, books };
}
export async function loadLedger(path: string): Promise<ReadingLedger> {
  try { return decodeLedger(await readFile(path, 'utf8')); }
  catch (error: unknown) {
    if (error instanceof Error && 'code' in error && error.code === 'ENOENT') return emptyLedger();
    throw error;
  }
}
export async function saveLedger(path: string, ledger: ReadingLedger): Promise<void> {
  const temporary = join(dirname(path), `.${Date.now()}-${process.pid}.reading-ledger.tmp`);
  await writeFile(temporary, encodeLedger(ledger), { encoding: 'utf8', flag: 'wx' });
  await rename(temporary, path);
}
