import os
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TARGET_GROUP_ID = int(os.getenv('TARGET_GROUP_ID', 0))
OPEN_TIME = os.getenv('OPEN_TIME', '07:00')
CLOSE_TIME = os.getenv('CLOSE_TIME', '22:00')
WELCOME_MESSAGE = os.getenv('WELCOME_MESSAGE', 'Welcome {username} to our group!')

# Group rules text (moved from .env to fix parsing issues)
GROUP_RULES = """📋 ПРАВИЛА ПУБЛИКАЦИИ ДЛЯ УЧАСТНИКОВ ЧАТА:

🔸 Каждому участнику доступно две публикации в сутки. Распределяйте время размещения верно!
🔸 Нельзя создавать несколько профилей и писать с них одно сообщение. За это моментальный бан!

🚫 ЗАПРЕЩЕНО:
❗ Материалы порнографического характера
❗ Политика, митинги, массовки
❗ Любые виды ставок
❗ Эскорт, веб-модели и проституция - бан без права обратного доступа
❗ Регистрации за деньги, реферальные ссылки
❗ Сетевой маркетинг и Пирамиды
❗ Реклама товаров и услуг
❗ Ссылки на чаты и каналы
❗ Брачные агентства - только на платной основе через @VICTORY_67
❗ Злоупотребление Caps Lock-ом и смайлами

⚠️ ЗА НАРУШЕНИЕ ПРАВИЛ - БАН!

📏 Размер публикации - не больше 300 символов! Проверить можно здесь: http://simvoli.net/

📝 Шаблон для вакансий:
1. Название вакансии
2. Название компании и сфера деятельности
3. Требования (образование/опыт/навыки)
4. Обязанности
5. Условия работы (часы/доход/преимущества)
6. Контактный номер телефона

⚡ Придерживайтесь шаблона, иначе - удаление вакансии, а позже бан!
📖 Пишите вакансии внятно и без ошЫбок.

💡 Думайте, прежде чем писать и проверьте, прежде чем отправлять!

🔐 Администрация оставляет за собой право редактировать правила и выбирать меру наказания."""

# Global variables
is_group_open = True
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))

class AdminBot:
    def __init__(self):
        self.bot = bot
        
    async def start_command(self, message: types.Message):
        """Handle /start command"""
        await message.answer(f'Hello {message.from_user.first_name}! I am an admin bot for group management.')
        
    async def help_command(self, message: types.Message):
        """Handle /help command"""
        help_text = """
**Bot Commands:**

**For Admins:**
/open - Open group for messages
/close - Close group for messages
/status - Show group status
/rules - Show group rules

**For Everyone:**
/rules - Show group rules
/help - Show this help
/start - Start interaction with bot
        """
        await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)
        
    async def rules_command(self, message: types.Message):
        """Show group rules"""
        await message.answer(GROUP_RULES)
        
    async def status_command(self, message: types.Message):
        """Show group status"""
        global is_group_open
        status = "Open" if is_group_open else "Closed"
        await message.answer(f'Group status: {status}')
        
    async def open_group_command(self, message: types.Message):
        """Open group"""
        if not await self.is_admin(message):
            return
            
        await self.set_group_permissions(True)
        await message.answer('Group opened for messages!')
        
    async def close_group_command(self, message: types.Message):
        """Close group"""
        if not await self.is_admin(message):
            return
            
        await self.set_group_permissions(False)
        await message.answer('Group closed for messages!')
            
    async def is_admin(self, message: types.Message) -> bool:
        """Check if user is admin"""
        try:
            chat_member = await bot.get_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id
            )
            
            if chat_member.status in ['administrator', 'creator']:
                return True
            else:
                await message.answer('This command is only for administrators!')
                return False
        except Exception as e:
            logger.error(f'Error checking admin status: {e}')
            return False
            
    async def set_group_permissions(self, allow_messages: bool):
        """Set group permissions"""
        global is_group_open
        try:
            if allow_messages:
                permissions = ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False
                )
            else:
                permissions = ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                )
                
            await bot.set_chat_permissions(TARGET_GROUP_ID, permissions)
            is_group_open = allow_messages
            logger.info(f'Group permissions set to: {"Open" if allow_messages else "Closed"}')
            
        except Exception as e:
            logger.error(f'Error setting permissions: {e}')
            
    async def handle_new_chat_members(self, message: types.Message):
        """Handle new chat members"""
        # Delete the system message about new member joining
        try:
            await message.delete()
            logger.info(f'Deleted system message about new member joining')
        except Exception as e:
            logger.error(f'Error deleting system message: {e}')
        
        for new_member in message.new_chat_members:
            # Skip if the new member is our bot
            if new_member.id == bot.id:
                continue
                
            username = new_member.first_name
            welcome_text = f"{WELCOME_MESSAGE.format(username=username)}\n\n{GROUP_RULES}"
            
            try:
                welcome_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=welcome_text
                )
                logger.info(f'Welcome message sent to {username}')
                
                # Schedule welcome message deletion after 4 minutes
                await asyncio.sleep(240)  # 4 minutes = 240 seconds
                try:
                    await bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=welcome_message.message_id
                    )
                    logger.info(f'Welcome message deleted after 4 minutes for {username}')
                except Exception as delete_error:
                    logger.error(f'Error deleting welcome message: {delete_error}')
                    
            except Exception as e:
                logger.error(f'Error sending welcome message: {e}')
                
    async def handle_messages(self, message: types.Message):
        """Handle messages - filter bots"""
        # Check if sender is a bot (but not our bot)
        if message.from_user.is_bot and message.from_user.id != bot.id:
            try:
                await message.delete()
                logger.info(f'Deleted message from bot: {message.from_user.first_name}')
                
                # Try to kick the bot from group
                try:
                    await bot.ban_chat_member(
                        chat_id=message.chat.id,
                        user_id=message.from_user.id
                    )
                    logger.info(f'Kicked bot: {message.from_user.first_name}')
                except Exception as kick_error:
                    logger.error(f'Error kicking bot: {kick_error}')
                    
            except Exception as e:
                logger.error(f'Error deleting bot message: {e}')
                
    async def scheduled_open_group(self):
        """Scheduled group open"""
        try:
            await self.set_group_permissions(True)
            
            # Send morning motivational message
            morning_message = """Доброе утро🙂
Сегодня это тот день, когда каждый может найти работу,
сотрудника и хорошее настроение😇
Берегите себя и своих близких!!"""
            
            message = await bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=morning_message
            )
            
            # Schedule message deletion after 30 minutes
            await asyncio.sleep(1800)  # 30 minutes = 1800 seconds
            try:
                await bot.delete_message(
                    chat_id=TARGET_GROUP_ID,
                    message_id=message.message_id
                )
                logger.info('Morning message deleted after 30 minutes')
            except Exception as delete_error:
                logger.error(f'Error deleting morning message: {delete_error}')
            
            logger.info('Group opened by schedule at 07:01')
        except Exception as e:
            logger.error(f'Error opening group by schedule: {e}')
            
    async def scheduled_close_group(self):
        """Scheduled group close"""
        try:
            await self.set_group_permissions(False)
            silence_message = """Добрый вечер🙂
С 22:00 до 7:00 у Вас нет возможности писать.
Внимательно прочтите правила группы.
Берегите себя и своих близких!"""
            
            await bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=silence_message
            )
            logger.info('Group closed by schedule at 22:00 - silence mode activated')
        except Exception as e:
            logger.error(f'Error closing group by schedule: {e}')
            
    async def periodic_rules_reminder(self):
        """Send periodic rules reminder every 4 hours"""
        try:
            reminder_message = """Пожалуйста, соблюдайте правила группы.
Берегите себя и своих близких!"""
            
            await bot.send_message(
                chat_id=TARGET_GROUP_ID,
                text=reminder_message
            )
            logger.info('Rules reminder sent to group')
        except Exception as e:
            logger.error(f'Error sending rules reminder: {e}')

# Create bot instance
admin_bot = AdminBot()

# Register command handlers
dp.message.register(admin_bot.start_command, Command("start"))
dp.message.register(admin_bot.help_command, Command("help"))
dp.message.register(admin_bot.rules_command, Command("rules"))
dp.message.register(admin_bot.status_command, Command("status"))
dp.message.register(admin_bot.open_group_command, Command("open"))
dp.message.register(admin_bot.close_group_command, Command("close"))

# Register message handlers
dp.message.register(admin_bot.handle_new_chat_members, F.new_chat_members)
dp.message.register(admin_bot.handle_messages)

async def setup_scheduler():
    """Setup APScheduler"""
    # Parse times (override open time to 07:01 as requested)
    open_hour, open_minute = 7, 1  # 07:01
    close_hour, close_minute = map(int, CLOSE_TIME.split(':'))
    
    # Add scheduled tasks
    scheduler.add_job(
        admin_bot.scheduled_open_group,
        CronTrigger(hour=open_hour, minute=open_minute, timezone='Europe/Moscow'),
        id='open_group',
        name='Open group at 07:01',
        replace_existing=True
    )
    
    scheduler.add_job(
        admin_bot.scheduled_close_group,
        CronTrigger(hour=close_hour, minute=close_minute, timezone='Europe/Moscow'),
        id='close_group',
        name='Close group at 22:00',
        replace_existing=True
    )
    
    # Add periodic rules reminder at specific times: 11:00, 15:00, 19:00
    scheduler.add_job(
        admin_bot.periodic_rules_reminder,
        CronTrigger(hour=11, minute=0, timezone='Europe/Moscow'),
        id='rules_reminder_11',
        name='Rules reminder at 11:00',
        replace_existing=True
    )
    
    scheduler.add_job(
        admin_bot.periodic_rules_reminder,
        CronTrigger(hour=15, minute=0, timezone='Europe/Moscow'),
        id='rules_reminder_15',
        name='Rules reminder at 15:00',
        replace_existing=True
    )
    
    scheduler.add_job(
        admin_bot.periodic_rules_reminder,
        CronTrigger(hour=19, minute=0, timezone='Europe/Moscow'),
        id='rules_reminder_19',
        name='Rules reminder at 19:00',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info('Scheduler started')

async def main():
    """Main function"""
    if not BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file!")
        return
        
    if not TARGET_GROUP_ID:
        print("Error: TARGET_GROUP_ID not found in .env file!")
        return
    
    # Setup scheduler
    await setup_scheduler()
    
    # Start bot
    logger.info('Bot started!')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
