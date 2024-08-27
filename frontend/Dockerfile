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

# Faqat production uchun kerakli paketlarni o'rnating
RUN npm install --only=production

EXPOSE 3000

CMD ["npm", "start"]
