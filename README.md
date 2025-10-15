# 📝 FastAPI Blog Backend

Бэкенд-приложение на **FastAPI** с использованием **PostgreSQL**, **SQLAlchemy (async)**, **Alembic**, **Poetry** и **Docker**.

---

## 🚀 Основные возможности

- Авторизация и регистрация пользователей (JWT)
- Разделение ролей (администратор / пользователь)
- Работа с постами (CRUD)
- Поддержка Docker и Docker Compose
- Миграции базы данных через Alembic
- Тесты с Pytest и httpx

---

## 🧩 Стек технологий

- **Python 3.11**
- **FastAPI**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL**
- **Poetry**
- **Docker / Docker Compose**
- **Pytest**

---

## ⚙️ Установка и запуск

### 1. Клонирование проекта
```bash
git clone https://github.com/ButakovIlya/testovoe.git
cd fastapi-blog-backend
```

### 2. Запуск проекта через Docker
```bash
docker compose up --build
```

После успешного запуска приложение будет доступно по адресу:

👉 **http://localhost**

### 3. Остановка контейнеров
```bash
docker compose down
```

---

## 📘 Документация API

Swagger-документация доступна по адресу:
```
http://localhost/docs
```
---

## 👨‍💻 Автор

**Илья Бутаков**  
Проект разработан с использованием принципов чистой архитектуры,  
асинхронного взаимодействия и модульного тестирования.
