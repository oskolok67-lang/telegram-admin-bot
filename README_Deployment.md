# Развертывание Telegram бота на облачных сервисах

## 🚀 Инструкция по развертыванию бота 24/7

### 📋 Что создано для развертывания:

- **Dockerfile** - для контейнеризации
- **railway.toml** - конфигурация для Railway
- **Procfile** - конфигурация для Heroku
- **.gitignore** - исключение лишних файлов
- **.dockerignore** - исключение файлов из Docker

---

## 🛠️ Варианты развертывания:

### 1. Railway (Рекомендуется)

**Преимущества:**
- Бесплатный план
- Автоматическое развертывание из GitHub
- Поддержка переменных окружения
- Стабильная работа 24/7

**Шаги:**
1. Создайте репозиторий на GitHub
2. Загрузите код в репозиторий
3. Зарегистрируйтесь на [Railway](https://railway.app)
4. Нажмите "Deploy New" → "Deploy from GitHub repo"
5. Выберите ваш репозиторий
6. Добавьте переменные окружения в Railway:
   - `TELEGRAM_BOT_TOKEN` = ваш токен
   - `TARGET_GROUP_ID` = ID вашей группы
7. Нажмите "Deploy"

### 2. Heroku

**Преимущества:**
- Бесплатный план
- Простота настройки
- Поддержка Python

**Шаги:**
1. Создайте репозиторий на GitHub
2. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Выполните команды:
   ```bash
   heroku create your-bot-name
   heroku config:set TELEGRAM_BOT_TOKEN=ваш_токен
   heroku config:set TARGET_GROUP_ID=ваш_id_группы
   git push heroku main
   ```

### 3. Render

**Преимущества:**
- Бесплатный план
- Поддержка Docker
- Стабильная работа

**Шаги:**
1. Создайте репозиторий на GitHub
2. Зарегистрируйтесь на [Render](https://render.com)
3. Нажмите "New" → "Web Service"
4. Подключите GitHub репозиторий
5. Настройте:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Добавьте переменные окружения

---

## 📤 Загрузка на GitHub:

### 1. Инициализация Git:
```bash
git init
git add .
git commit -m "Initial commit - Telegram Admin Bot"
```

### 2. Создание репозитория на GitHub:
1. Зайдите на [GitHub](https://github.com)
2. Нажмите "New repository"
3. Назовите репозиторий (например: `telegram-admin-bot`)
4. Скопируйте URL репозитория

### 3. Отправка кода:
```bash
git remote add origin https://github.com/username/telegram-admin-bot.git
git branch -M main
git push -u origin main
```

---

## 🔧 Настройка переменных окружения:

### Railway:
- Зайдите в настройки проекта
- Перейдите в "Variables"
- Добавьте:
  - `TELEGRAM_BOT_TOKEN`: `1901727624:AAFhMmisKPuXG5C1e_wOm6_hqmpNLmoIRkk`
  - `TARGET_GROUP_ID`: `-1001563184444`

### Heroku:
```bash
heroku config:set TELEGRAM_BOT_TOKEN=1901727624:AAFhMmisKPuXG5C1e_wOm6_hqmpNLmoIRkk
heroku config:set TARGET_GROUP_ID=-1001563184444
```

### Render:
- В настройках сервиса → "Environment"
- Добавьте те же переменные

---

## ✅ Проверка развертывания:

1. Бот должен появиться в Telegram как онлайн
2. Проверьте команды `/start`, `/help`, `/status`
3. Убедитесь, что планировщик работает (проверьте логи)

---

## 🐛 Устранение проблем:

### Бот не запускается:
- Проверьте правильность токена
- Убедитесь, что все переменные окружения установлены
- Проверьте логи развертывания

### Планировщик не работает:
- Убедитесь, что часовой пояс установлен правильно
- Проверьте, что APScheduler установлен

### Проблемы с правами:
- Убедитесь, что бот имеет права администратора в группе
- Проверьте ID группы

---

## 📞 Поддержка:

Если возникнут проблемы:
1. Проверьте логи на облачном сервисе
2. Убедитесь, что все переменные окружения правильные
3. Проверьте, что бот имеет права в группе

---

## 🎉 Готово!

После развертывания ваш бот будет работать 24/7 без необходимости держать компьютер включенным.
