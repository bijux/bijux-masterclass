export function createClient(config) {
  if (!config || typeof config.baseUrl !== "string" || typeof config.token !== "string") {
    throw new TypeError("baseUrl and token are required");
  }
  if (!config.baseUrl.startsWith("https://") && !config.baseUrl.startsWith("http://127.0.0.1")) {
    throw new Error("baseUrl must be HTTPS outside the loopback laboratory");
  }
  return Object.freeze({ baseUrl: config.baseUrl, token: config.token });
}
