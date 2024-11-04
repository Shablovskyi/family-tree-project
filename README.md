# Family Tree Project

## Опис проекту

**Family Tree Project** – це веб-застосунок для побудови та візуалізації генеалогічного дерева. Проект дозволяє користувачам додавати членів родини, встановлювати родинні зв’язки та переглядати родинне дерево в інтерактивному інтерфейсі. Фронтенд розроблено на React, а бекенд на Flask.

## Основні функції

- Додавання нових членів родини.
- Встановлення родинних зв’язків (батько, мати, діти).
- Візуалізація генеалогічного дерева.
- Можливість редагування та видалення даних.

## Технології

- **Frontend**: React, React Router, Axios
- **Backend**: Flask, Flask-CORS
- **Database**: (за потреби) SQLAlchemy з PostgreSQL або SQLite
- **Інші бібліотеки**: Redux, D3, react-dnd (опціонально)

## Структура проекту

family-tree-project/ ├── backend/ │   ├── app.py                     # Основний файл бекенду │   ├── requirements.txt            # Залежності Python │   ├── models/                     # Моделі бази даних │   ├── routes/                     # Ендпоїнти API │   └── utils/                      # Допоміжні функції ├── frontend/ │   ├── public/ │   ├── src/ │   │   ├── components/             # React компоненти │   │   ├── pages/                  # Сторінки додатка │   │   ├── services/               # Запити до API │   │   └── styles/                 # CSS стилі ├── .gitignore └── README.md

## Встановлення

1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/your-username/family-tree-project.git
   cd family-tree-project

2. Налаштування фронтенду:

cd frontend
npm install


3. Налаштування бекенду:

cd ../backend
python3 -m venv venv            # Створення віртуального середовища
source venv/bin/activate        # Активація віртуального середовища
pip install -r requirements.txt # Встановлення залежностей



Запуск проекту

1. Запуск бекенду на Flask:

cd backend
flask run


2. Запуск фронтенду на React:

cd frontend
npm start



Бекенд буде запущено за адресою http://127.0.0.1:5000, а фронтенд за адресою http://localhost:3000.

Використання

Відкрийте фронтенд за адресою http://localhost:3000.

Додавайте членів родини, встановлюйте зв’язки та переглядайте генеалогічне дерево в реальному часі.


Майбутні вдосконалення

Пошук членів родини по дереву.

Додавання інтерактивної візуалізації зв'язків.

Аутентифікація та багатокористувацька підтримка.


Автори

Ваше ім’я - GitHub


Ліцензія

Цей проект ліцензовано відповідно до MIT License - див. LICENSE для деталей.

Тепер у вас є повний файл README.md, який можна скопіювати та вставити у ваш проект.
