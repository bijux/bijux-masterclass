interface BaseReview { readonly text: string; readonly author: string }
export interface Draft extends BaseReview { readonly state: 'draft' }
export interface InReview extends BaseReview { readonly state: 'in-review'; readonly submittedAt: string; readonly reviewer: string }
export interface Approved extends BaseReview { readonly state: 'approved'; readonly submittedAt: string; readonly reviewer: string; readonly decidedAt: string; readonly note?: string }
export interface Rejected extends BaseReview { readonly state: 'rejected'; readonly submittedAt: string; readonly reviewer: string; readonly decidedAt: string; readonly reason: string }
export type Review = Draft | InReview | Approved | Rejected;

export function submit(draft: Draft, reviewer: string, submittedAt: string): InReview {
  if (reviewer.trim() === '') throw new Error('reviewer must not be empty');
  return { ...draft, state: 'in-review', reviewer: reviewer.trim(), submittedAt };
}

export function approve(review: InReview, decidedAt: string, note?: string): Approved {
  return note === undefined
    ? { ...review, state: 'approved', decidedAt }
    : { ...review, state: 'approved', decidedAt, note };
}

export function reject(review: InReview, decidedAt: string, rawReason: string): Rejected {
  const reason = rawReason.trim();
  if (reason === '') throw new Error('reason must not be empty');
  return { ...review, state: 'rejected', decidedAt, reason };
}

function assertNever(value: never): never { throw new Error(`unhandled review ${JSON.stringify(value)}`); }

export function renderReview(review: Review): string {
  switch (review.state) {
    case 'draft': return `draft\t${review.author}`;
    case 'in-review': return `in-review\t${review.reviewer}\t${review.submittedAt}`;
    case 'approved': return `approved\t${review.reviewer}\t${review.decidedAt}`;
    case 'rejected': return `rejected\t${review.reviewer}\t${review.reason}`;
    default: return assertNever(review);
  }
}
