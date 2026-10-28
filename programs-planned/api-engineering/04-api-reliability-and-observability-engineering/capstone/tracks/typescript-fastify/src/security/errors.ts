export class SecurityControlError extends Error {
  readonly code: string;
  readonly status: number;

  constructor(code: string, detail: string, status = 400) {
    super(detail);
    this.name = "SecurityControlError";
    this.code = code;
    this.status = status;
  }
}
