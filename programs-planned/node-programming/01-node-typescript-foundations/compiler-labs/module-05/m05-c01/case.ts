type Task = { state: 'open'; title: string } | { state: 'done'; title: string; finishedAt: string };
function describe(task: Task): string {
  switch (task.state) {
    case 'open': return task.title;
    case 'done': return `${task.title} @ ${task.finishedAt}`;
  }
}
console.log(describe({ state: 'open', title: 'types' }));
