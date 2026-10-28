export interface RuntimeSample {
  wallNs: bigint;
  cpuUserMicros: number;
  cpuSystemMicros: number;
}

export function measureCallable<T>(operation: () => T): {
  value: T;
  sample: RuntimeSample;
} {
  const cpuBefore = process.cpuUsage();
  const wallBefore = process.hrtime.bigint();
  const value = operation();
  const wallAfter = process.hrtime.bigint();
  const cpu = process.cpuUsage(cpuBefore);
  return {
    value,
    sample: {
      wallNs: wallAfter - wallBefore,
      cpuUserMicros: cpu.user,
      cpuSystemMicros: cpu.system,
    },
  };
}
