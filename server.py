import sqlite3
from aiogram import Bot, Dispatcher, types

# daha gelismis istiyorsan https://t.me/sekomirson yaz

BOT_TOKEN = "TELEGRAM_TOKEN"

DB_FILE = "tavuk_ciftligi.db"

# Komutlar
START_COMMAND = "/start"
BUY_CHICKEN_COMMAND = "/al"
SELL_EGG_COMMAND = "/sat"
EXPAND_COMMAND = "/buyut"

CHICKEN_PRICE = 100
EGG_PRICE = 5

EGG_RATE = 0.5

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

connection = sqlite3.connect(DB_FILE)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    money INTEGER DEFAULT 0,
    chickens INTEGER DEFAULT 0,
    eggs INTEGER DEFAULT 0
)""")
connection.commit()

@dp.message_handler(commands=START_COMMAND)
async def start(message: types.Message):
    user_id = message.from_user.id
  
    cursor.execute(f"SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(f"INSERT INTO users (user_id) VALUES (?)", (user_id,))
        connection.commit()

    await message.reply(
        "Tavuk Çiftliğine hoş geldin! Tavuk alıp yumurta satarak para kazanabilirsin. Ne yapmak istiyorsun?"
    )
  
@dp.message_handler(commands=BUY_CHICKEN_COMMAND)
async def buy_chicken(message: types.Message):
    user_id = message.from_user.id
  
    cursor.execute(f"SELECT money FROM users WHERE user_id = ?", (user_id,))
    money = cursor.fetchone()[0]
    if money < CHICKEN_PRICE:
        await message.reply("Tavuk alacak kadar paran yok!")
        return
      
    cursor.execute(f"UPDATE users SET money = money - ?, chickens = chickens + 1 WHERE user_id = ?", (CHICKEN_PRICE, user_id))
    connection.commit()

    await message.reply(f"1 tavuk satın aldın! Şimdi {cursor.fetchone()[2]} tavuğun var.")
  
@dp.message_handler(commands=SELL_EGG_COMMAND)
async def sell_egg(message: types.Message):
    user_id = message.from_user.id
  
    cursor.execute(f"SELECT eggs FROM users WHERE user_id = ?", (user_id,))
    eggs = cursor.fetchone()[0]
    if eggs == 0:
        await message.reply("Yumurtan yok!")
        return
      
    earned_money = eggs * EGG_PRICE
    cursor.execute(f"UPDATE users SET money = money + ?, eggs = eggs - {eggs} WHERE user_id = ?", (earned_money, user_id))
    connection.commit()

    await message.reply(f"{eggs} yumurta sattın ve {earned_money} para kazandın! Paran: {cursor.fetchone()[0]}")
  
@dp.message_handler(commands=EXPAND_COMMAND)
async def expand(message: types.Message):
    user_id = message.from_user.id
  
    cursor.execute(f"SELECT money FROM users WHERE user_id = ?", (user_id,))
    money = cursor.fetchone()[0]
    if money < EXPANSION_COST:
        await message.reply("Çiftliği genişletmek için paran yok!")
        return

# daha gelismis istiyorsan https://t.me/sekomirson yaz
