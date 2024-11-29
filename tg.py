import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import random
import datetime


with open('TOKEN.txt', 'r') as f:
    token = f.read().strip()

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())


predictions = [
  "Сегодня вас ждет удачный день, полный приятных сюрпризов!",
  "Вас ждет удача в любви и творчестве. Не бойтесь рисковать!",
  "Звезды сулят вам финансовый успех и благополучие.",
  "Постарайтесь сегодня быть внимательнее к своим близким. Они нуждаются в вас.",
  "Ваши мечты сбудутся. Только верьте в себя!",
  "Этот день полон возможностей для новых начинаний. Не упустите свой шанс!",
  "Сегодня вы будете полны энергии и энтузиазма. Используйте этот день с пользой!",
  "Вас ждет день, полный радости и веселья. Наслаждайтесь моментом!",
  "Вас ждет успех в делах и гармония в личной жизни. Отличного дня!",
  "Не бойтесь быть собой, и мир откроет перед вами свои объятия.",
]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
  await message.answer(
    "Привет! Введи свою дату рождения (дд.мм.гггг), чтобы получить короткое предсказание на сегодня."
  )

@dp.message_handler(state=None)
async def handle_message(message: types.Message):
  try:
    date_parts = message.text.split('.')
    day = int(date_parts[0])
    month = int(date_parts[1])
    year = int(date_parts[2])
    if len(str(year)) != 4:
        await message.answer("Неправильная дата рождения! Введите ее в формате дд.мм.гггг.")
        return

    birthdate = datetime.date(year, month, day)

    if birthdate > datetime.date.today():
      await message.answer("Неправильная дата рождения! Введите ее в формате дд.мм.гггг.")
      return

    user_name = message.from_user.first_name

    random_prediction = random.choice(predictions)

    await message.answer(
      f"{user_name}, вот короткое предсказание на сегодня для тебя: {random_prediction}"
    )

  except Exception as _:
    await message.answer(
      "Неправильный формат даты! Введите ее в формате дд.мм.гггг."
    )

if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)