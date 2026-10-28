interface App { readonly load: () => Promise<string> }
const app: App = { load: async () => 'a' };
app.load = async () => 'b';
