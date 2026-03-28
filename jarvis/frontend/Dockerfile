# 1-bosqich: Build bosqichi
FROM node:18-alpine AS builder

# Ishchi papkani o'rnatish
WORKDIR /app

# package.json va package-lock.json fayllarini nusxalash
COPY package.json package-lock.json* ./

# Kutubxonalarni o'rnatish
RUN npm install

# Butun frontend kodini nusxalash
COPY . .

# Next.js ilovasini build qilish
RUN npm run build

# 2-bosqich: Ishga tushirish bosqichi
FROM node:18-alpine

WORKDIR /app

# Build qilingan fayllarni nusxalash
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Ilova ishga tushadigan port
EXPOSE 3000

# Ilovani ishga tushirish
CMD ["npm", "start"]