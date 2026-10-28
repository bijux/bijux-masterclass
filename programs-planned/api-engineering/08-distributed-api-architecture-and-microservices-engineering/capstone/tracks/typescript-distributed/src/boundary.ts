export interface BoundaryCandidate {
  name: string;
  ownership: number;
  dataAutonomy: number;
  changeIndependence: number;
  scaleIsolation: number;
  failureIsolation: number;
  securityBoundary: number;
  operationalCost: number;
  synchronousCoupling: number;
}

export type BoundaryDecision =
  | "extract"
  | "conditional"
  | "keep-together"
  | "reject";

export function weightedScore(candidate: BoundaryCandidate): number {
  return 3 * candidate.ownership +
    3 * candidate.dataAutonomy +
    2 * candidate.changeIndependence +
    2 * candidate.scaleIsolation +
    2 * candidate.failureIsolation +
    2 * candidate.securityBoundary -
    3 * candidate.operationalCost -
    3 * candidate.synchronousCoupling;
}

export function boundaryDecision(candidate: BoundaryCandidate): BoundaryDecision {
  if (candidate.dataAutonomy <= 0) return "reject";
  const score = weightedScore(candidate);
  if (score >= 14) return "extract";
  if (score >= 8) return "conditional";
  return "keep-together";
}
