type Task = { state: 'open'; title: string } | { state: 'done'; title: string; finishedAt: string };
function date(task: Task): string {
  return task.finishedAt;
}
console.log(date({ state: 'open', title: 'types' }));
