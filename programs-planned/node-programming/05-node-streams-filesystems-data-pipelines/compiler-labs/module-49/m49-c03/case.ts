type Outcome = { readonly branch: 'archive'; readonly status: 'committed' } | { readonly branch: 'index'; readonly status: 'failed'; readonly message: string };
const value: Outcome = { branch: 'archive', status: 'committed' };
void value;
