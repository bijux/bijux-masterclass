export type Phase = "starting" | "accepting" | "draining" | "stopping" | "stopped";

export class Lifecycle {
  private current: Phase = "starting";
  private active = 0;

  public phase(): Phase { return this.current; }
  public activeCalls(): number { return this.active; }
  public serving(): boolean { return this.current === "accepting"; }

  public start(): void {
    if (this.current !== "starting") throw new Error("invalid transition");
    this.current = "accepting";
  }

  public admit(): () => void {
    if (this.current !== "accepting") throw new Error("not accepting");
    this.active += 1;
    let released = false;
    return () => {
      if (released) throw new Error("permit already released");
      released = true;
      this.active -= 1;
      if (this.active < 0) throw new Error("active call underflow");
      if (this.current === "stopping" && this.active === 0) {
        this.current = "stopped";
      }
    };
  }

  public drain(): void {
    if (this.current !== "accepting" && this.current !== "draining") {
      throw new Error("invalid drain transition");
    }
    this.current = "draining";
  }

  public stop(): void {
    this.current = this.active === 0 ? "stopped" : "stopping";
  }
}
