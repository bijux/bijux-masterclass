export class TokenBucket {
  readonly #capacity:number; readonly #refillPerSecond:number; #tokens:number; #lastMs=0; readonly #scale=1_000_000;
  constructor(capacityUnits:number,refillUnitsPerSecond:number){if(capacityUnits<=0||refillUnitsPerSecond<0)throw new Error("invalid bucket configuration");this.#capacity=capacityUnits*this.#scale;this.#refillPerSecond=refillUnitsPerSecond*this.#scale;this.#tokens=this.#capacity;}
  allow(nowMs:number,costUnits=1):boolean{if(!Number.isSafeInteger(nowMs)||nowMs<this.#lastMs||costUnits<=0)throw new Error("invalid token-bucket input");const elapsed=nowMs-this.#lastMs;this.#tokens=Math.min(this.#capacity,this.#tokens+Math.floor(elapsed*this.#refillPerSecond/1000));this.#lastMs=nowMs;const cost=costUnits*this.#scale;if(this.#tokens<cost)return false;this.#tokens-=cost;return true;}
}
export class ConcurrencyLimiter { #inUse=0; constructor(readonly limit:number){if(limit<=0)throw new Error("limit must be positive");} get inUse():number{return this.#inUse;} tryAcquire():Permit|undefined{if(this.#inUse>=this.limit)return undefined;this.#inUse+=1;return new Permit(()=>{if(this.#inUse<=0)throw new Error("permit accounting underflow");this.#inUse-=1;});}}
export class Permit { #released=false; constructor(private readonly releaseFn:()=>void){} release():void{if(!this.#released){this.releaseFn();this.#released=true;}} }
