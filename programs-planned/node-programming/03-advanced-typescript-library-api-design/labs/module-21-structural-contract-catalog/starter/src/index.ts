export interface FeatureDefinition { readonly id: string; readonly label: string }
export function listFeatureIds(features: readonly FeatureDefinition[]): readonly string[] {
  return features.map((feature) => feature.id);
}
