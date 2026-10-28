try {
  throw new Error('broken');
} catch (error: unknown) {
  console.log(error.message);
}
