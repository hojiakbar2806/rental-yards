# Build Stage
FROM node:18 AS builder

WORKDIR /app

# Avval package.json va package-lock.json-ni ko'chiring, 
# chunki bu fayllar o'zgarishi kamroq ehtimolga ega
COPY package.json package-lock.json ./

# Paketlarni o'rnating
RUN npm install

# Dastur kodini ko'chiring
COPY . .

# Ilovani build qiling
RUN npm run build

# Production Stage
FROM node:18-slim

WORKDIR /app

# Faqat kerakli fayllarni ko'chiring
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/package-lock.json ./package-lock.json

# Faqat production uchun kerakli paketlarni o'rnating
RUN npm install --only=production

EXPOSE 3000

CMD ["npm", "start"]
