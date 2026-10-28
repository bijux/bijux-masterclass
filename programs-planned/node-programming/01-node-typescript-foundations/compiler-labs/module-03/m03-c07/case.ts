let render: (value: number) => string;
if (Math.random() > 0.5) render = String;
console.log(render(3));
