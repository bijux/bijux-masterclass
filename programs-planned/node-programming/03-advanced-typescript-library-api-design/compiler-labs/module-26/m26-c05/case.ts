interface Counter{increment(step?:number):number;value():number}const counter:Counter={increment:step=>step??1,value:()=>0};console.log(counter.increment());
