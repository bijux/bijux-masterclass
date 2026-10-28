import { inspect } from 'node:util';
export const RUNTIME_META = Symbol('objectatlas.runtime-meta');
export const NODE_INTERNAL = Symbol('objectatlas.node-internal');
export const ATLAS_INSPECT = inspect.custom;
