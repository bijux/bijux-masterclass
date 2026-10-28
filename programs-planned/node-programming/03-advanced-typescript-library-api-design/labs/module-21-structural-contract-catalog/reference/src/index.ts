export type Stability = 'experimental' | 'stable' | 'deprecated';
export interface FeatureDefinition { readonly id: string; readonly label: string; readonly stability: Stability }
export type FeatureId<F extends readonly FeatureDefinition[]> = F[number]['id'];
export type FeatureById<F extends readonly FeatureDefinition[], I extends FeatureId<F>> = Extract<F[number], { readonly id: I }>;
export interface FeatureCatalog<F extends readonly FeatureDefinition[]> {
  readonly features: F;
  ids(): readonly FeatureId<F>[];
  get<I extends FeatureId<F>>(id: I): FeatureById<F, I>;
}
export function defineCatalog<const F extends readonly FeatureDefinition[]>(...features: F): FeatureCatalog<F> {
  const byId = new Map<string, FeatureDefinition>();
  for (const feature of features) {
    if (feature.id.trim() === '') throw new Error('feature id must not be empty');
    if (byId.has(feature.id)) throw new Error(`duplicate feature id: ${feature.id}`);
    byId.set(feature.id, Object.freeze({ ...feature }));
  }
  const stable = Object.freeze([...features]) as unknown as F;
  return Object.freeze({
    features: stable,
    ids: () => Object.freeze(stable.map((feature) => feature.id)) as readonly FeatureId<F>[],
    get<I extends FeatureId<F>>(id: I): FeatureById<F, I> {
      const value = byId.get(id);
      if (value === undefined) throw new Error(`unknown feature: ${id}`);
      return value as FeatureById<F, I>;
    },
  });
}
