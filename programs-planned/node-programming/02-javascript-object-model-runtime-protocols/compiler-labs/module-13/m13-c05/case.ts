class Pair { constructor(readonly left: number, readonly right: number) {} }
const RightPair = Pair.bind(null, 3);
console.log(new RightPair(4).left + new RightPair(4).right);
