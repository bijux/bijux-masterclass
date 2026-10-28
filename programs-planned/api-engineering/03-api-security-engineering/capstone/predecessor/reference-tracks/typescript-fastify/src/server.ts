import { buildApp } from "./app.js";
import { settingsFromEnvironment } from "./config.js";

async function main(): Promise<void> {
  const settings = settingsFromEnvironment();
  const app = await buildApp(settings);
  const host = process.env["HOST"] ?? "0.0.0.0";
  const port = Number.parseInt(process.env["PORT"] ?? "8001", 10);

  let closing = false;
  const close = async (signal: NodeJS.Signals): Promise<void> => {
    if (closing) return;
    closing = true;
    app.log.info({ signal }, "shutdown requested");
    await app.close();
  };

  process.once("SIGTERM", () => {
    void close("SIGTERM");
  });
  process.once("SIGINT", () => {
    void close("SIGINT");
  });

  await app.listen({ host, port });
}

main().catch((error: unknown) => {
  console.error(error);
  process.exitCode = 1;
});
