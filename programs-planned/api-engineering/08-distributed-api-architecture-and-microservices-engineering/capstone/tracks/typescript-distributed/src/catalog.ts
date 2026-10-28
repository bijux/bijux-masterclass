import { ValidationError } from "./model.js";

export interface ServiceDefinition {
  name: string;
  owner: string;
  kind: string;
  dataFacts: ReadonlySet<string>;
  interfaces: ReadonlySet<string>;
}

export class ServiceCatalog {
  readonly services = new Map<string, ServiceDefinition>();

  add(service: ServiceDefinition): void {
    if (this.services.has(service.name)) {
      throw new ValidationError(`duplicate service: ${service.name}`);
    }
    if (!service.owner) {
      throw new ValidationError(`owner required: ${service.name}`);
    }
    this.services.set(service.name, service);
  }

  ownerOf(fact: string): string {
    const owners = [...this.services.values()]
      .filter((service) => service.dataFacts.has(fact))
      .map((service) => service.name);
    if (owners.length !== 1) {
      throw new ValidationError(`fact has ${owners.length} owners: ${fact}`);
    }
    return owners[0]!;
  }

  validateSingleWriters(): void {
    const facts = new Set(
      [...this.services.values()].flatMap((service) => [...service.dataFacts]),
    );
    for (const fact of facts) this.ownerOf(fact);
  }

  validateNoTableServices(): void {
    for (const name of [
      "project-service",
      "dataset-table-service",
      "idempotency-service",
    ]) {
      if (this.services.has(name)) {
        throw new ValidationError(`table-shaped service rejected: ${name}`);
      }
    }
  }
}
