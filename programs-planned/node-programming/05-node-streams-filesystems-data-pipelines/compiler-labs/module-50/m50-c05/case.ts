interface Report { readonly inputBytes: number; readonly outputBytes: number; readonly inputSha256: string; readonly outputSha256: string; }
const report: Report = { inputBytes: 1, outputBytes: 1, inputSha256: 'a', outputSha256: 'b' };
void report;
