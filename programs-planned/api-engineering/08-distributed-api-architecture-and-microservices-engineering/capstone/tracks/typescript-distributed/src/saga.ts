import { Conflict, ValidationError } from "./model.js";

export type SagaState =
  | "new"
  | "artifact-stored"
  | "completed"
  | "compensation-required"
  | "compensated";

export class ArtifactCompletionSaga {
  state: SagaState = "new";
  artifactId?: string;
  readonly processed = new Set<string>();
  readonly history: string[] = [];

  constructor(
    readonly sagaId: string,
    readonly runId: string,
    readonly attemptId: string,
  ) {}

  recordArtifact(
    eventId: string,
    artifactId: string,
    attemptId: string,
  ): "duplicate" | "stored" | "compensate" {
    if (this.processed.has(eventId)) return "duplicate";
    this.processed.add(eventId);
    if (attemptId !== this.attemptId) {
      this.state = "compensation-required";
      this.artifactId = artifactId;
      this.history.push("stale-artifact");
      return "compensate";
    }
    if (this.state !== "new" && this.state !== "artifact-stored") {
      throw new Conflict(`cannot record artifact in ${this.state}`);
    }
    if (this.artifactId && this.artifactId !== artifactId) {
      throw new Conflict("saga already bound to another artifact");
    }
    this.artifactId = artifactId;
    this.state = "artifact-stored";
    this.history.push("artifact-stored");
    return "stored";
  }

  complete(
    commandId: string,
    currentAttemptId: string,
  ): "duplicate" | "completed" | "compensate" {
    if (this.processed.has(commandId)) return "duplicate";
    this.processed.add(commandId);
    if (this.state === "completed") return "duplicate";
    if (this.state !== "artifact-stored" || !this.artifactId) {
      throw new Conflict("artifact must be stored before completion");
    }
    if (currentAttemptId !== this.attemptId) {
      this.state = "compensation-required";
      this.history.push("stale-completion");
      return "compensate";
    }
    this.state = "completed";
    this.history.push("run-completed");
    return "completed";
  }

  compensate(actionId: string): "duplicate" | "compensated" {
    if (this.processed.has(actionId)) return "duplicate";
    this.processed.add(actionId);
    if (this.state !== "compensation-required") {
      throw new ValidationError("compensation is not required");
    }
    this.state = "compensated";
    this.history.push("artifact-orphaned");
    return "compensated";
  }
}
