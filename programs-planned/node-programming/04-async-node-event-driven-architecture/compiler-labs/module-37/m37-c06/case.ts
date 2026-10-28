import{channel}from'node:diagnostics_channel';const c=channel<{runId:string}>('x');c.publish({taskId:'t'});export {};
