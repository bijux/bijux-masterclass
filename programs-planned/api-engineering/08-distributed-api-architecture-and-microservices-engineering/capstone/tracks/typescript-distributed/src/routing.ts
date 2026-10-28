import { Unavailable, ValidationError } from "./model.js";

export interface Instance {
  instanceId: string;
  service: string;
  version: string;
  healthy: boolean;
  accepting: boolean;
}

export class ServiceRegistry {
  private readonly instances = new Map<string, Instance[]>();
  private readonly cursor = new Map<string, number>();

  register(instance: Instance): void {
    const list = this.instances.get(instance.service) ?? [];
    if (list.some((item) => item.instanceId === instance.instanceId)) {
      throw new ValidationError("duplicate instance id");
    }
    this.instances.set(instance.service, [...list, instance]);
  }

  setHealth(service: string, instanceId: string, healthy: boolean): void {
    const found = (this.instances.get(service) ?? [])
      .find((item) => item.instanceId === instanceId);
    if (!found) throw new ValidationError("unknown instance");
    found.healthy = healthy;
  }

  choose(service: string, supportedVersions?: ReadonlySet<string>): Instance {
    const candidates = (this.instances.get(service) ?? [])
      .filter((item) => item.healthy && item.accepting)
      .filter((item) => !supportedVersions || supportedVersions.has(item.version))
      .sort((left, right) => left.instanceId.localeCompare(right.instanceId));
    if (candidates.length === 0) {
      throw new Unavailable(`no healthy instance for ${service}`);
    }
    const index = (this.cursor.get(service) ?? 0) % candidates.length;
    this.cursor.set(service, index + 1);
    return candidates[index]!;
  }
}
