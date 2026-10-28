const a=new Promise(r=>setTimeout(()=>r('a'),5));const b=Promise.resolve('b');const x=await Promise.allSettled([a,b]);console.log(x.map(v=>v.status==='fulfilled'?v.value:'x').join(','));
