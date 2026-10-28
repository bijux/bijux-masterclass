const dictionary = Object.create(null) as Record<string, number>;
dictionary['count'] = 1;
console.log(Object.getPrototypeOf(dictionary) === null, dictionary['count']);
