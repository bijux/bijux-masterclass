const model={name:'Ada'};const key='name' as const;const event={type:`${key}Changed`,previous:model[key],current:'Grace'};console.log(`${event.type}:${event.previous}->${event.current}`);
