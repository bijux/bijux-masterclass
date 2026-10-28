type T={kind:'echo';text:string}|{kind:'delay';ms:number};function run(t:T){switch(t.kind){case'echo':return t.text;case'delay':return String(t.ms);}}void run;export {};
