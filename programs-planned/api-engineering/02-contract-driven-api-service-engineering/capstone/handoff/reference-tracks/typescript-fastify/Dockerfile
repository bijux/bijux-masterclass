FROM node:24.19.0-bookworm-slim AS build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --ignore-scripts
COPY tsconfig.json ./
COPY src ./src
RUN npm run build

FROM node:24.19.0-bookworm-slim
ENV NODE_ENV=production
WORKDIR /app
RUN useradd --system --uid 10001 --create-home analysis
COPY package.json package-lock.json* ./
RUN npm install --omit=dev --ignore-scripts && npm cache clean --force
COPY --from=build /app/dist ./dist
COPY migrations ./migrations
COPY fixtures ./fixtures
RUN mkdir -p /data/artifacts && chown -R analysis:analysis /app /data
USER analysis
EXPOSE 8001
CMD ["node", "dist/src/server.js"]
