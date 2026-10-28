const nested = { value: 1 };
const outer = Object.freeze({ nested });
nested.value = 2;
console.log(outer.nested.value);
