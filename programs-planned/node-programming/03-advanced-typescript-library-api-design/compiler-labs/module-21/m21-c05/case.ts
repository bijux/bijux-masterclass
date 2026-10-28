declare const userBrand:unique symbol;type UserId=string&{readonly[userBrand]:'UserId'};const parse=(s:string):UserId=>s as UserId;const id:UserId=parse('u1');console.log(id);
