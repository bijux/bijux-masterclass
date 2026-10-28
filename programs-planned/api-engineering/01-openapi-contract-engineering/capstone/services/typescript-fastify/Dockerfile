FROM node:22-slim
WORKDIR /app
COPY package.json ./
RUN npm install --ignore-scripts
COPY tsconfig.json ./
COPY src ./src
EXPOSE 3000
CMD ["npm", "run", "start"]
