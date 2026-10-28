export interface StageContract {
    readonly name: string;
    readonly input: string;
    readonly output: string;
    readonly owner: string;
    readonly bound: string;
    readonly completion: string;
}
export function missingFields(stage: Partial<StageContract>): readonly string[] { return ['name', 'input', 'output', 'owner', 'bound', 'completion'].filter(k => !(k in stage)); }
