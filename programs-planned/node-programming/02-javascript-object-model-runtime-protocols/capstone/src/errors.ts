export class ObjectAtlasError extends Error {
  constructor(message: string, options?: ErrorOptions) { super(message, options); this.name = new.target.name; }
}
export class ValidationError extends ObjectAtlasError {}
export class UnknownNodeError extends ObjectAtlasError { constructor(id: string) { super(`unknown node: ${id}`); } }
export class DuplicateNodeError extends ObjectAtlasError { constructor(id: string) { super(`duplicate node: ${id}`); } }
export class IllegalGraphTransitionError extends ObjectAtlasError {}
export class TraversalInvalidatedError extends ObjectAtlasError { constructor() { super('atlas structure changed during traversal'); } }
export class DraftClosedError extends ObjectAtlasError { constructor(state: string) { super(`attribute draft is ${state}`); } }
export class DecodeError extends ObjectAtlasError {}
export class StorageError extends ObjectAtlasError {}
export class CommandError extends ObjectAtlasError {}
