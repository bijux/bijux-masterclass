export interface Principal {
  readonly subject: string;
  readonly tenant: string;
  readonly scopes: ReadonlySet<string>;
  readonly roles: ReadonlySet<string>;
  readonly clientId?: string;
  readonly tokenId?: string;
  readonly assurance: "baseline" | "high" | string;
  readonly authAgeSeconds: number;
}

export interface ResourceFacts {
  readonly tenant?: string;
  readonly owner?: string;
  readonly members: ReadonlySet<string>;
  readonly creator?: string;
  readonly status?: string;
  readonly attributes?: Readonly<Record<string, unknown>>;
}

export interface Decision {
  readonly allowed: boolean;
  readonly reason: string;
  readonly conceal: boolean;
  readonly obligations: readonly string[];
}
