async function* values(){throw new Error('sequence failed');} void (async()=>{for await(const value of values()){void value;}})();
