export interface Reading { readonly celsius: number }
export function fromCelsius(celsius: number): Reading { return { celsius }; }
