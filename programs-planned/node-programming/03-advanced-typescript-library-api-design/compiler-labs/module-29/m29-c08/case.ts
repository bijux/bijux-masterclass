interface Client{fetch(id:string):string}const client={fetch(_id:string){throw new Error('legacy endpoint removed');}}satisfies Client;console.log(client.fetch('1'));
