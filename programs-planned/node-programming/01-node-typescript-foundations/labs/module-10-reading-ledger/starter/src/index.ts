export interface QueuedBook { readonly state: 'queued'; readonly id: number; readonly title: string }
export function queueBook(id: number, title: string): QueuedBook {
  const normalized = title.trim();
  if (normalized === '') throw new Error('title must not be empty');
  return { state: 'queued', id, title: normalized };
}
