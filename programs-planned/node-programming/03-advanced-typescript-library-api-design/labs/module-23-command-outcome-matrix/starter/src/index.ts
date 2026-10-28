export type Command={readonly kind:'ping'}|{readonly kind:'length';readonly text:string};
export function commandKind(command:Command):Command['kind']{return command.kind;}
