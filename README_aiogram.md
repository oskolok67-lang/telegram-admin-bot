# Telegram Administrative Bot (aiogram 3.x)

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

## Technical details

### Schedule configuration
- Uses **APScheduler** with **AsyncIOScheduler**
- **CronTrigger** for precise timing
- **Europe/Moscow** timezone (UTC+3)
- **Persistent** job scheduling

### aiogram 3.x features
- **Modern async/await** syntax
- **Magic filters** (`F.new_chat_members`)
- **Command filters** (`Command("start")`)
- **Dispatcher** registration system
- **ParseMode** support for Markdown

### Configuration management
- **Environment variables** via `.env` file
- **python-dotenv** for loading
- **Template strings** for personalization
- **Default values** for missing config

## Additional configuration

### Change working hours
Edit variables in `.env`:
```env
OPEN_TIME=08:00  # Open time (HH:MM format)
CLOSE_TIME=22:00 # Close time (HH:MM format)
```

### Customize rules
Change `GROUP_RULES` variable in `.env` file. Supports multiline text.

### Customize welcome message
Change `WELCOME_MESSAGE` variable in `.env` file. Use `{username}` placeholder for personalization.

## Troubleshooting

### Bot doesn't respond to commands
1. Check token correctness in `.env`
2. Make sure bot is running
3. Check bot rights in group
4. Verify aiogram 3.x installation

### Automatic open/close not working
1. Check time format in `.env` (HH:MM)
2. Make sure bot has permission to change permissions
3. Check target group ID
4. Verify timezone settings

### Bot messages not being deleted
1. Make sure bot has delete message rights
2. Check that bot is administrator
3. Verify bot protection logic

### Scheduler not working
1. Check APScheduler installation
2. Verify timezone configuration
3. Check job registration in logs

## Dependencies

- **aiogram 3.4.1** - Telegram bot framework
- **python-dotenv 1.0.0** - Environment variable management
- **apscheduler 3.10.4** - Task scheduling
- **pytz 2023.3** - Timezone handling

## License

MIT License

## Support

If you have problems, create an issue in the repository or contact the developer.
