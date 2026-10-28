class Base { value = 'base-field'; constructor() { console.log(this.value); } }
class Derived extends Base { override value = 'derived-field'; constructor() { super(); console.log(this.value); } }
new Derived();
