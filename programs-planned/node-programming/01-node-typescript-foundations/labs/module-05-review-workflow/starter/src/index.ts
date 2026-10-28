export interface Draft {
  readonly state: 'draft';
  readonly text: string;
  readonly author: string;
}

export function wordCount(draft: Draft): number {
  return draft.text.trim() === '' ? 0 : draft.text.trim().split(/\s+/u).length;
}
