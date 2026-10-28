import { createHash } from 'node:crypto';
const digest: string = createHash('sha256').update('x').digest('hex');
void digest;
