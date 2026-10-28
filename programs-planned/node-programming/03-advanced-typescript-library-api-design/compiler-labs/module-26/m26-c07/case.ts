const createCounter=(initial=0)=>{let value=initial;return{increment(step=1){value+=step;return value;}}};console.log(createCounter(2).increment(3));
