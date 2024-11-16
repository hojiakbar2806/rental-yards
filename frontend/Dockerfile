FROM node:20-alpine AS dependencies

WORKDIR /app

COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS build

WORKDIR /app

COPY . .

RUN npm run build

RUN npm prune --production && npm cache clean --force

FROM node:20-alpine AS production

WORKDIR /app

COPY --from=build /app/package*.json ./
RUN npm ci --only=production

COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public

EXPOSE 3000

CMD ["npm", "start"]
