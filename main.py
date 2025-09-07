import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
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
    await message.answer(
        "👋 Salom! Ismingiz va familyangizni kiriting:\n"
        "Masalan: `Ali Karimov` yoki `Karimov Ali`"
    )

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
        return await message.answer("⛔ Sizda ruxsat yo‘
