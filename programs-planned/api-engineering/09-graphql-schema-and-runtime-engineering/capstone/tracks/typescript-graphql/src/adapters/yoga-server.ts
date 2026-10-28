/** Optional GraphQL Yoga adapter; excluded from the dependency-light build. */
import { createServer } from "node:http";
import { createSchema, createYoga } from "graphql-yoga";
const typeDefs = /* GraphQL */ `type Query { health: String! }`;
const yoga = createYoga({schema:createSchema({typeDefs,resolvers:{Query:{health:()=>"ok"}}})});
createServer(yoga).listen(4000);
