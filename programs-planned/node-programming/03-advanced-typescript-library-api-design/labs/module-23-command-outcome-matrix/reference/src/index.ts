export type Command=
 |{readonly kind:'ping'}
 |{readonly kind:'length';readonly text:string}
 |{readonly kind:'divide';readonly numerator:number;readonly denominator:number};
export type Outcome<C extends Command>=C extends{readonly kind:'ping'}?'pong':C extends{readonly kind:'length'}?number:C extends{readonly kind:'divide'}?{readonly ok:true;readonly value:number}|{readonly ok:false;readonly reason:'division-by-zero'}:never;
export function execute<C extends Command>(command:C):Outcome<C>{
  switch(command.kind){
    case'ping':return'pong' as Outcome<C>;
    case'length':return command.text.length as Outcome<C>;
    case'divide':return(command.denominator===0?{ok:false,reason:'division-by-zero'}:{ok:true,value:command.numerator/command.denominator}) as Outcome<C>;
  }
}
export function assertNever(value:never):never{throw new Error(`unhandled command: ${JSON.stringify(value)}`);}
