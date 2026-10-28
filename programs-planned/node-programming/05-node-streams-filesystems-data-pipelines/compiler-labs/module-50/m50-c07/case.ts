const completed = [{ index: 2, value: 'c' }, { index: 0, value: 'a' }, { index: 1, value: 'b' }];
completed.sort((left, right) => left.index - right.index);
console.log(completed.map(item => item.value).join(''));
