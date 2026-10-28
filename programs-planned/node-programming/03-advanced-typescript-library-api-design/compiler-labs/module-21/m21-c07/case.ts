interface View{readonly count:number}
const source={count:1};const view:View=source;source.count=2;console.log(view.count);
