const packageIdentity = {
  type: 'module',
  private: true,
} satisfies { type: 'module' | 'commonjs'; private: boolean };
const mode: 'module' = packageIdentity.type;
console.log(mode);
