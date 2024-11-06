# Вибір базового образу з Node.js для збірки React-додатка
FROM node:16 as build

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо package.json і package-lock.json для встановлення залежностей
COPY package.json package-lock.json ./

# Встановлюємо залежності
RUN npm install

# Копіюємо весь проєкт в робочу директорію
COPY . .

# Створюємо збірку React-додатка
RUN npm run build

# Вибір базового образу для розгортання з Nginx
FROM nginx:alpine

# Копіюємо збірку з попереднього етапу в директорію, яку обслуговує Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Копіюємо налаштування Nginx (опціонально, якщо потрібно налаштувати редиректи)
# COPY nginx.conf /etc/nginx/nginx.conf

# Відкриваємо порт 80 для доступу до додатка
EXPOSE 80

# Запуск Nginx
CMD ["nginx", "-g", "daemon off;"]