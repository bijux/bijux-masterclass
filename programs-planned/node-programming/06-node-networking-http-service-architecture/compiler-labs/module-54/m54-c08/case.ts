const media: string = process.env.MEDIA ?? 'text/plain';
if (media !== 'application/json') throw new Error('unsupported media type');
