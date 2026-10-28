type T={kind:'echo';text:string}|{kind:'delay';ms:number};function run(t:T):string{if(t.kind==='echo')return t.text;}void run;export {};
