class NodeValue { constructor(readonly id: string) {} toRecord() { return { id: this.id }; } }
const live = new NodeValue('a');
const record = live.toRecord();
console.log(live instanceof NodeValue, record instanceof NodeValue);
