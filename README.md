# Telegram Административный Бот

🤖 Бот для автоматического администрирования Telegram каналов и групп с возможностью управления доступом, приветствия новых участников и фильтрации сообщений.

## 🚀 Функционал

### Telegram Administrative Bot (aiogram 3.x)

Bot for automatic administration of Telegram groups with access management, new member greeting, and bot filtering capabilities using aiogram 3.x and APScheduler.

## Features

### Main features:
- **Automatic group open/close by schedule** (07:00-20:00 Moscow time UTC+3)
- **Bot protection** - automatic deletion of bot messages and kicking bots
- **New member greeting** with personalized welcome and group rules
- **Group rules management** with customizable messages
- **Administrative commands** for group management

### Bot commands:

#### For administrators:
- `/open` - Open group for messages
- `/close` - Close group for messages  
- `/status` - Show current group status
- `/rules` - Show group rules

#### For all participants:
- `/rules` - Show group rules
- `/help` - Show command help
- `/start` - Start interaction with bot

## Requirements

- Python 3.8+
- Bot token from @BotFather
- Admin rights in target group

## Installation and setup

### 1. Clone and install dependencies

```bash
git clone <repository-url>
cd Bot_2
pip install -r requirements.txt
```

### 2. Create bot

1. Find [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` command
3. Follow instructions to create bot
4. Save the token

### 3. Configure environment variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TARGET_GROUP_ID=your_target_group_id

# Schedule configuration (Moscow timezone UTC+3)
OPEN_TIME=07:00
CLOSE_TIME=20:00

# Group rules text
GROUP_RULES=Welcome to our group! Please follow the rules:
1. Be respectful to other members
2. No spam or flooding
3. No offensive language
4. Stay on topic

# Welcome message template (use {username} for personalization)
WELCOME_MESSAGE=Welcome {username} to our group!
```

### 4. Get group ID

To get group ID:
1. Add [@userinfobot](https://t.me/userinfobot) to Telegram
2. Send him a message in the target group
3. He will show the group ID

### 5. Add bot to group

1. Add bot to target group
2. Give bot admin rights:
   - Delete messages
   - Ban users
   - Manage invite links
   - Change info (optional)

## Running

```bash
python bot.py
```

Bot will start and work automatically. APScheduler will handle scheduled tasks.

## Features details

### Automatic access management
- **Group opens** at 07:00 Moscow time (UTC+3)
- **Group closes** at 20:00 Moscow time (UTC+3)
- **Notifications** sent on open/close with time stamps
- **Timezone aware** scheduling using APScheduler

### Bot protection
- **Automatic deletion** of messages from other bots
- **Auto-kick** bots that try to send messages
- **Logging** of all bot protection actions
- **Excludes** the admin bot itself from filtering

### New member greeting
- **Personalized welcome** with member's first name
- **Group rules** sent with welcome message
- **Automatic** detection of new members
- **Skips** bot's own join message

### Administrative functions
- **Admin rights verification** before command execution
- **Permission management** for group access control
- **Status tracking** of group open/closed state
- **Error handling** with logging

## 🔧 Дополнительная настройка

### Изменение времени работы
Отредактируйте переменные в `.env`:
```env
OPEN_TIME=08:00  # Время открытия
CLOSE_TIME=22:00 # Время закрытия
```

### Кастомизация правил
Измените переменную `CHANNEL_RULES` в `.env` файле.

### Кастомизация приветствия
Измените переменную `WELCOME_MESSAGE` в `.env` файле.

## 🐛 Устранение проблем

### Бот не отвечает на команды
1. Проверьте правильность токена в `.env`
2. Убедитесь, что бот запущен
3. Проверьте права бота в канале/группе

### Не работает автоматическое открытие/закрытие
1. Проверьте формат времени в `.env` (HH:MM)
2. Убедитесь, что у бота есть права на изменение разрешений
3. Проверьте ID целевого канала

### Не удаляются сообщения от ботов
1. Убедитесь, что у бота есть права на удаление сообщений
2. Проверьте, что бот является администратором

## 📄 Лицензия

MIT License

## 🤝 Поддержка

При возникновении проблем создайте issue в репозитории или свяжитесь с разработчиком.
