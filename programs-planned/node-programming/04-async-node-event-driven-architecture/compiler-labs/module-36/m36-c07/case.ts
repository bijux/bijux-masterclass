async function* values(){try{yield 1;yield 2;}finally{console.log('closed');}} void (async()=>{for await(const value of values()){void value;break;}})();
