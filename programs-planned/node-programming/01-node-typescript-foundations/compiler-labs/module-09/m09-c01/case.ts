console.log('sync');
Promise.resolve().then(() => console.log('promise'));
setTimeout(() => console.log('timer'), 0);
