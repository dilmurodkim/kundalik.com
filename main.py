import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiohttp import web

from config import BOT_TOKEN, ADMIN_ID, WEBHOOK_URL, PORT
from database import init_db, add_user, list_users, delete_user, find_user
from utils import clean_name

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# === Start komandasi ===
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("👋 Salom! Ismingiz va familyangizni kiriting:\n"
                         "Masalan: `Ali Karimov` yoki `Karimov Ali`")

# === O‘quvchi qo‘shish ===
@dp.message(Command("add_student"))
async def add_student(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Sizda ruxsat yo‘q!")
    try:
        _, ism, familya, login, parol = message.text.split()
    except:
        return await message.answer("❌ Foydalanish: /add_student Ism Familya login parol")

    add_user(clean_name(ism), clean_name(familya), login, parol, "o‘quvchi")
    await message.answer(f"✅ O‘quvchi qo‘shildi: {ism.title()} {familya.title()}")

# === O‘qituvchi qo‘shish ===
@dp.message(Command("add_teacher"))
async def add_teacher(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Sizda ruxsat yo‘q!")
    try:
        _, ism, familya, login, parol = message.text.split()
    except:
        return await message.answer("❌ Foydalanish: /add_teacher Ism Familya login parol")

    add_user(clean_name(ism), clean_name(familya), login, parol, "o‘qituvchi")
    await message.answer(f"✅ O‘qituvchi qo‘shildi: {ism.title()} {familya.title()}")

# === Ro‘yxat ===
@dp.message(Command("list"))
async def cmd_list(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Sizda ruxsat yo‘q!")

    users = list_users()
    if not users:
        return await message.answer("📂 Bazada foydalanuvchi yo‘q.")

    text = "📋 Foydalanuvchilar ro‘yxati:\n\n"
    for i, (ism, familya, login, parol, rol) in enumerate(users, start=1):
        text += (f"{i}. 👤 {ism.title()} {familya.title()}\n"
                 f"   🎓 Rol: {rol}\n"
                 f"   🔑 Login: {login} | Parol: {parol}\n\n")
    await message.answer(text)

# === O‘chirish ===
@dp.message(Command("delete"))
async def cmd_delete(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Sizda ruxsat yo‘q!")
    try:
        _, ism, familya = message.text.split()
    except:
        return await message.answer("❌ Foydalanish: /delete Ism Familya")

    deleted = delete_user(clean_name(ism), clean_name(familya))
    if deleted:
        await message.answer(f"🗑️ {ism.title()} {familya.title()} o‘chirildi.")
    else:
        await message.answer("❌ Bunday foydalanuvchi topilmadi.")

# === Oddiy foydalanuvchi ===
@dp.message(F.text)
async def get_user(message: Message):
    parts = message.text.split()
    if len(parts) != 2:
        return await message.answer("❌ Iltimos, faqat Ism va Familya kiriting.")

    a, b = clean_name(parts[0]), clean_name(parts[1])

    user = find_user(a, b) or find_user(b, a)
    if user:
        login, parol, rol = user
        await message.answer(f"👤 {parts[0].title()} {parts[1].title()} ({rol})\n"
                             f"🔑 Login: {login}\n"
                             f"🔒 Parol: {parol}")
    else:
        await message.answer("❌ Bunday foydalanuvchi topilmadi.")

# === Webhook handler ===
async def handle(request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return web.Response()

# === Asosiy ishga tushirish ===
async def main():
    init_db()
    app = web.Application()
    app.router.add_post("/webhook", handle)

    # Telegram webhookni sozlash
    await bot.set_webhook(WEBHOOK_URL)

    logging.info("🤖 Bot webhook rejimida ishlayapti...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
