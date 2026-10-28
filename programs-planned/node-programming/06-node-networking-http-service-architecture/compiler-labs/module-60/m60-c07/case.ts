export interface Runtime { readonly endpoints:Readonly<Record<string,string>>; close():Promise<{readonly cleanupErrors:readonly string[]}> }
