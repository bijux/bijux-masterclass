import { buildApp } from "./app.js";

const app = await buildApp();
const port = Number.parseInt(process.env["PORT"] ?? "3000", 10);
const host = process.env["HOST"] ?? "127.0.0.1";

try {
  await app.listen({ host, port });
} catch (error) {
  app.log.error(error);
  process.exitCode = 1;
}
