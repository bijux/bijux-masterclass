const input={user:{age:'old'}};const age=(input as{user?:{age?:unknown}}).user?.age;if(typeof age!=='number')console.log('$.user.age:expected number');
