class Base {}
class Derived extends Base { constructor() { console.log(this); super(); } }
new Derived();
