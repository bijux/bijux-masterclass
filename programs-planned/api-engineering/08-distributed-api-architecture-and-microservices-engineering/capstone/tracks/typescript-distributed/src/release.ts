import { ValidationError } from "./model.js";

interface Version {
  major: number;
  minor: number;
}

export type VersionClassification =
  | "compatible"
  | "compatible-with-feature-disabled"
  | "reject";

function parse(value: string): Version {
  const match = /^(\d+)\.(\d+)$/u.exec(value);
  if (!match) throw new ValidationError(`invalid version: ${value}`);
  return {
    major: Number(match[1]),
    minor: Number(match[2]),
  };
}

export class VersionPolicy {
  classify(consumer: string, provider: string): VersionClassification {
    const consumerVersion = parse(consumer);
    const providerVersion = parse(provider);
    if (consumerVersion.major !== providerVersion.major) return "reject";
    if (consumerVersion.minor <= providerVersion.minor) return "compatible";
    if (consumerVersion.minor === providerVersion.minor + 1) {
      return "compatible-with-feature-disabled";
    }
    return "reject";
  }
}
