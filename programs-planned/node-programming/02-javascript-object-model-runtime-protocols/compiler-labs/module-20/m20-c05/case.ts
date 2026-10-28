class NodeValue { constructor(readonly id: string) {} label() { return this.id.toUpperCase(); } }
const decoded = JSON.parse(JSON.stringify(new NodeValue('a'))) as NodeValue;
console.log(decoded.label());
