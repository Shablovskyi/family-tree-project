# Базовий образ з Python
FROM python:3.10-slim

# Встановлюємо залежності для системи (наприклад, psycopg2 потребує додаткових бібліотек)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файли вимог (requirements.txt) і встановлюємо залежності
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код додатка в контейнер
COPY . .

# Встановлюємо змінні середовища для Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Відкриваємо порт 5000 для доступу до додатка Flask
EXPOSE 5000

# Запускаємо додаток
CMD ["flask", "run"]