type Ctor<T = object> = new (...args: any[]) => T;
function WithTag<TBase extends Ctor>(Base: TBase) { return class extends Base { tag = 'x'; }; }
class Base {}
const Tagged = WithTag(Base);
console.log(new Tagged().tag);
