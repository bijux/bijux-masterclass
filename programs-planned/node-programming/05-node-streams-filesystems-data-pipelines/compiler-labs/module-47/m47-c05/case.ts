import { createGzip, createGunzip } from 'node:zlib';
const stages = [createGzip(), createGunzip()] as const;
void stages;
