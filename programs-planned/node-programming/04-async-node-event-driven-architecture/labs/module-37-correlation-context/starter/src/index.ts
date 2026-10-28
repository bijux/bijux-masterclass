export interface Context { readonly runId: string; readonly taskId?: string; }
export function childContext(parent: Context, taskId: string): Context {
  return Object.freeze({ runId: parent.runId, taskId });
}
