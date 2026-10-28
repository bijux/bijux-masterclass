interface J{run:(signal:AbortSignal)=>Promise<number>}const jobs:readonly J[]=[{run:async()=>1}];void jobs;export {};
