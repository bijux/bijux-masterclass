const nanMatches = Object.is(Number.NaN, Number.NaN);
const zeroMatches = Object.is(0, -0);
console.log(nanMatches, zeroMatches);
