class Lease implements Disposable { [Symbol.dispose](): void { console.log('closed'); } }
const lease: Disposable = new Lease();
lease[Symbol.dispose]();
