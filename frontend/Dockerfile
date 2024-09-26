# Dependencies bosqichi
FROM node:20-alpine AS dependencies

WORKDIR /app

# Zaruriy build kutubxonalarni o'rnatish (python3, g++, make)
RUN apk add --no-cache python3 g++ make

COPY package*.json ./
RUN npm ci

# Build bosqichi
FROM node:20-alpine AS build

WORKDIR /app

# Hamma loyihani nusxalash
COPY . .

# Loyihani build qilish
RUN npm run build

# Production uchun keraksiz paketlarni olib tashlash va kechani tozalash
RUN npm prune --production && npm cache clean --force

# Production bosqichi
FROM node:20-alpine AS production

WORKDIR /app

# Faqat zarur paketlarni o'rnatish
COPY --from=dependencies /app/package*.json ./
RUN npm ci --only=production

# Build qilingan fayllarni nusxalash
COPY --from=build /app/.next ./.next
COPY --from=build /app/public ./public

# 3000 portni ochish
EXPOSE 3000

# Next.js serverini ishga tushirish
CMD ["npm", "start"]
