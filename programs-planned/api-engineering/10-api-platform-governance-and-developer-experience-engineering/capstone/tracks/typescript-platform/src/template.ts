export interface TemplateParameter { name: string; pattern?: string; enum?: string[]; minLength?: number; }
export interface TemplateSpec { parameters: TemplateParameter[]; outputs: string[]; }

export function validateParameters(params: Record<string,string>, spec: TemplateSpec): void {
  for (const rule of spec.parameters) {
    const value = params[rule.name];
    if (!value) throw new Error(`missing-parameter:${rule.name}`);
    if (rule.pattern && !(new RegExp(rule.pattern).test(value))) throw new Error(`invalid-parameter:${rule.name}`);
    if (rule.enum && !rule.enum.includes(value)) throw new Error(`invalid-parameter:${rule.name}`);
    if (rule.minLength !== undefined && value.length < rule.minLength) throw new Error(`invalid-parameter:${rule.name}`);
  }
}

export function renderText(template: string, params: Record<string,string>): string {
  let output = template;
  for (const [key, value] of Object.entries(params)) output = output.replaceAll(`{{${key}}}`, value);
  if (output.includes("{{") || output.includes("}}")) throw new Error("unresolved-placeholder");
  if (/(api[_-]?key|password|secret|token)\s*[:=]\s*["']?[A-Za-z0-9+/=_-]{8,}/i.test(output)) throw new Error("embedded-secret");
  return output;
}
