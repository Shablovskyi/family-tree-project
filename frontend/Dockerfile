# 1. Базовий образ
FROM node:18

# 2. Робоча директорія
WORKDIR /app

# 3. Копіюємо package.json та lock
COPY package*.json ./

# 4. Встановлення залежностей
RUN npm install

# 5. Копіюємо решту файлів
COPY . .

# 6. Старт розробки
CMD ["npm", "run", "dev"]
