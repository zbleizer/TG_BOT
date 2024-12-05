import logging
import datetime
import dataclasses

from email.message import Message
from aiogram import Bot, Dispatcher, types
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import asyncio
import random

from dataclasses import dataclass
from dateutil.parser import parse
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


PHYSICAL_CONST = 23.6884
EMOTIONAL_CONST = 28.426125
INTELLIGENT_CONST = 33.163812
HEART_CONST = 37.901499
CREATIVE_CONST = 42.6392
INTUITIVE_CONST = 47.3769
HIGHER_CONST = 52.1146


@dataclass
class BiorhythmCompatibility:
    first_birthdate: datetime.date
    second_birthdate: datetime.date

    def calculate_biorhythm(self, birthdate, period):
        days_since_birth = (datetime.date.today() - birthdate).days
        return days_since_birth % period

    def __post_init__(self) -> None:
        self.first_physical = self.calculate_biorhythm(self.first_birthdate, PHYSICAL_CONST)
        self.first_emotional = self.calculate_biorhythm(self.first_birthdate, EMOTIONAL_CONST)
        self.first_intelligent = self.calculate_biorhythm(self.first_birthdate, INTELLIGENT_CONST)
        self.first_heart = self.calculate_biorhythm(self.first_birthdate, HEART_CONST)
        self.first_creative = self.calculate_biorhythm(self.first_birthdate, CREATIVE_CONST)
        self.first_intuitive = self.calculate_biorhythm(self.first_birthdate, INTUITIVE_CONST)
        self.first_higher = self.calculate_biorhythm(self.first_birthdate, HIGHER_CONST)


        self.second_physical = self.calculate_biorhythm(self.second_birthdate, PHYSICAL_CONST)
        self.second_emotional = self.calculate_biorhythm(self.second_birthdate, EMOTIONAL_CONST)
        self.second_intelligent = self.calculate_biorhythm(self.second_birthdate, INTELLIGENT_CONST)
        self.second_heart = self.calculate_biorhythm(self.second_birthdate, HEART_CONST)
        self.second_creative = self.calculate_biorhythm(self.second_birthdate, CREATIVE_CONST)
        self.second_intuitive = self.calculate_biorhythm(self.second_birthdate, INTUITIVE_CONST)
        self.second_higher = self.calculate_biorhythm(self.second_birthdate, HIGHER_CONST)


        self.compatibility_percentage = self.calculate_compatibility()

    def calculate_compatibility(self) -> int:

        total_difference = (
            abs(self.first_physical - self.second_physical) +
            abs(self.first_emotional - self.second_emotional) +
            abs(self.first_intelligent - self.second_intelligent) +
            abs(self.first_heart - self.second_heart) +
            abs(self.first_creative - self.second_creative) +
            abs(self.first_intuitive - self.second_intuitive) +
            abs(self.first_higher - self.second_higher)
        )

        max_possible_difference = 7 * max(PHYSICAL_CONST, EMOTIONAL_CONST, INTELLIGENT_CONST, HEART_CONST, CREATIVE_CONST, INTUITIVE_CONST, HIGHER_CONST)
        compatibility = 100 - int((total_difference / max_possible_difference) * 100)
        return max(0, min(100, compatibility))


@dataclasses.dataclass
class Sector:
    digit: int | None
    title: str
    value: int

    def __str__(self):
        interpretation = self.interpret_value()
        return f"{self.title}: {self.value} ({interpretation})"

    def interpret_value(self):
        if self.title == "Характер" and self.value == 0:
            return "Пусто – редкий случай, следует приравнивать к 1."
        elif self.title == "Долг" and self.value >= 2:
            return "8/88 и более"
        elif self.value == 1:
            return "1 – мягкость, сниженные воля и ответственность, высокий статус."
        elif self.value == 2:
            return "11 – деликатный, вежливый, приятный, любит похвалу."
        elif self.value == 3:
            return "111 – золотая середина, адаптивность."
        elif self.value == 4:
            return "1111 – прирожденный лидер, инициативность."
        elif self.value == 5:
            return "11111 – диктатор, целеустремленность без препятствий."
        elif self.value == 6:
            return "111111 – перегруженный характер, завышенные амбиции, низкая целеустремленность."
        elif self.value >= 7:
            return "1111111 – усиленный контроль, избегание ответственности."
        else:
            return "Нет интерпретации."


def get_digit_sum(n: int) -> int:
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s



def zero_fill(number: int, width: int = 2) -> str:
    return str(number).zfill(width)


@dataclass
class PythagorasSquare:
    birthdate: datetime.date

    def __post_init__(self) -> None:
        self.string_birthdate = self.birthdate.strftime("%d%m%Y")
        self.digit_rows = self.get_digit_rows()
        self.sectors = self.calculate_sectors()


    def get_first_number(self) -> int:
        return get_digit_sum(int(self.string_birthdate))

    def get_second_number(self) -> int:
        return get_digit_sum(self.get_first_number())

    def get_third_number(self) -> int:
        return self.get_first_number() - int(self.string_birthdate[0]) * 2

    def get_fourth_number(self) -> int:
        return get_digit_sum(self.get_third_number())

    def get_digit_rows(self) -> list[list[int]]:
        second_row = (
            list(map(int, list(zero_fill(self.get_first_number()))))
            + list(map(int, list(zero_fill(self.get_second_number()))))
            + list(map(int, list(zero_fill(self.get_third_number()))))
            + list(map(int, list(zero_fill(self.get_fourth_number()))))
        )

        return [
            list(map(int, list(self.string_birthdate))),
            second_row
        ]

    def get_sector_value(self, digit: int) -> int:
        count = 0
        for row in self.digit_rows:
            count += row.count(digit)
        return count

    def get_additional_sector_value(self, sectors: list[Sector]) -> int:
        return sum(s.value for s in sectors)


    def calculate_sectors(self) -> list[Sector]:
        sectors = [
            Sector(digit=1, title="Характер", value=self.get_sector_value(1)),
            Sector(digit=2, title="Энергия", value=self.get_sector_value(2)),
            Sector(digit=3, title="Интерес", value=self.get_sector_value(3)),
            Sector(digit=4, title="Здоровье", value=self.get_sector_value(4)),
            Sector(digit=5, title="Логика", value=self.get_sector_value(5)),
            Sector(digit=6, title="Труд", value=self.get_sector_value(6)),
            Sector(digit=7, title="Удача", value=self.get_sector_value(7)),
            Sector(digit=8, title="Долг", value=self.get_sector_value(8)),
            Sector(digit=9, title="Память", value=self.get_sector_value(9)),
            Sector(digit=None, title="Самооценка", value=self.get_additional_sector_value([self.get_sector_value(1), self.get_sector_value(2), self.get_sector_value(3)])),
            Sector(digit=None, title="Быт", value=self.get_additional_sector_value([self.get_sector_value(4), self.get_sector_value(5), self.get_sector_value(6)])),
            Sector(digit=None, title="Талант", value=self.get_additional_sector_value([self.get_sector_value(7), self.get_sector_value(8), self.get_sector_value(9)])),
            Sector(digit=None, title="Цель", value=self.get_additional_sector_value([self.get_sector_value(1), self.get_sector_value(4), self.get_sector_value(7)])),
            Sector(digit=None, title="Семья", value=self.get_additional_sector_value([self.get_sector_value(2), self.get_sector_value(5), self.get_sector_value(8)])),
            Sector(digit=None, title="Привычки", value=self.get_additional_sector_value([self.get_sector_value(3), self.get_sector_value(6), self.get_sector_value(9)])),
            Sector(digit=None, title="Дух", value=self.get_additional_sector_value([self.get_sector_value(1), self.get_sector_value(5), self.get_sector_value(9)])),
            Sector(digit=None, title="Темперамент", value=self.get_additional_sector_value([self.get_sector_value(3), self.get_sector_value(5), self.get_sector_value(7)])),
        ]
        return sectors


    def __str__(self):
        return "\n".join(map(str, self.sectors))


class Form(StatesGroup):
    waiting_for_birthdate = State()
    waiting_for_first_birthdate = State()
    waiting_for_second_birthdate = State()
    waiting_for_birthdate2 = State()


with open('TOKEN.txt', 'r') as f:
    token = f.read().strip()

start_router = Router()
bot = Bot(token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.include_router(start_router)

logging.basicConfig(level=logging.INFO)

button_prediction = KeyboardButton(text="Получить предсказание 💌")
button_compatibility = KeyboardButton(text="Совместимость 💫")
button_help = KeyboardButton(text="❗️Помощь❗️")
button_pythogoras = KeyboardButton(text="🧩Квадрат Пифагора 🧩")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_prediction],
        [button_compatibility],
        [button_help],
        [button_pythogoras]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать!\n"
                         "Бот 🤍Влюбись🤍 откроет перед вами тайны совместимость с вашим партнером, "
                         "а также поделится предсказанием для тебя 💌\n\n", reply_markup=keyboard)


@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer(
        "Я могу поделиться предсказанием и рассчитать совместимость. Выберите 'Получить предсказание' или 'Совместимость'")


@dp.message()
async def handle_message(message: types.Message, state: FSMContext):
    if message.text == "Получить предсказание 💌":
        await state.set_state(Form.waiting_for_birthdate)
        await message.answer("Введите свою дату рождения (в формате ДД.ММ.ГГГГ):")

    elif message.text == "Совместимость 💫":
        await state.set_state(Form.waiting_for_first_birthdate)
        await message.answer("Введите первую дату рождения (в формате ДД.ММ.ГГГГ):")

    elif message.text == "🧩Квадрат Пифагора 🧩":
        await state.set_state(Form.waiting_for_birthdate2)
        await message.answer("Введите свою дату рождения (в формате ДД.ММ.ГГГГ):")

    elif message.text == "❗️Помощь❗️":
        await cmd_help(message)
    else:

        if await state.get_state() == Form.waiting_for_birthdate:
            await handle_birthdate(message, state)

        elif await state.get_state() == Form.waiting_for_first_birthdate:
            await process_first_birthdate(message, state)

        elif await state.get_state() == Form.waiting_for_second_birthdate:
            await process_second_birthdate(message, state)

        elif await state.get_state() == Form.waiting_for_birthdate2:
            await pyth_birthdate(message, state)


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


def calculate_compatibility(birthday1, birthday2):
    try:
        biorhythm_result = BiorhythmCompatibility(birthday1, birthday2)
        biorhythm_str = (biorhythm_result.calculate_compatibility())

        return (
            f"🤍Совместимость между {birthday1.strftime('%d.%m.%Y')} и {birthday2.strftime('%d.%m.%Y')} рассчитана 🤍\n"
            f"\nБиоритмы: {biorhythm_str}%\n"
        )

    except Exception as e:
        return f"Ошибка при расчете совместимости: {e}"


def calculate_square(birthday1):
    try:
        pythagoras1 = PythagorasSquare(birthday1)

        return (
            f"🧩Рассчет квадрата Пифагора 🧩\n"
            f"{pythagoras1}"
        )

    except Exception as e:
        return f"Ошибка при расчете квадрата Пифагора: {e}"


def validate_date(date_str):
    try:
        date = parse(date_str, dayfirst=True)
        if date > datetime.datetime.now():
            raise ValueError("Такой даты еще не было.")
        return date.date()

    except ValueError as e:
        raise ValueError(f"Invalid date: {e}")


@dp.message(StateFilter(Form.waiting_for_birthdate2))
async def pyth_birthdate(message: types.Message, state: FSMContext):
    try:
        birthdate = validate_date(message.text)
        result = calculate_square(birthdate)
        await message.answer(result)
        await state.clear()

    except (ValueError, IndexError):
        await message.answer("Неправильный формат даты! Введите ее в формате ДД.ММ.ГГГГ.")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")


@dp.message(StateFilter(Form.waiting_for_birthdate))
async def handle_birthdate(message: types.Message, state: FSMContext):
    try:
        birthdate = validate_date(message.text)
        user_name = message.from_user.first_name
        random_prediction = random.choice(predictions)
        await message.answer(f"{user_name}, вот предсказание: {random_prediction}")
        await state.clear()

    except (ValueError, IndexError):
        await message.answer("Неправильный формат даты! Введите ее в формате ДД.ММ.ГГГГ.")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")


@dp.message(StateFilter(Form.waiting_for_first_birthdate))
async def process_first_birthdate(message: types.Message, state: FSMContext):
    try:
        birthday1 = validate_date(message.text)
        await state.update_data(birthday1=birthday1)
        await message.answer("Введите вторую дату рождения (в формате ДД.ММ.ГГГГ):")
        await state.set_state(Form.waiting_for_second_birthdate)
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
    except Exception as e:
        logging.exception(f"An error occurred: {e}")


@dp.message(StateFilter(Form.waiting_for_second_birthdate))
async def process_second_birthdate(message: types.Message, state: FSMContext):
    try:
        birthday2 = validate_date(message.text)
        user_data = await state.get_data()
        birthday1 = user_data['birthday1']
        compatibility_result = calculate_compatibility(birthday1, birthday2)
        await message.answer(compatibility_result)
        await message.answer("Для получения более развернутой совместимости нажмите кнопку 'Оплатить'.",
                             reply_markup=payment_keyboard())
        await state.clear()

    except ValueError as e:
        await message.answer(f"Ошибка: {e}")

    except Exception as e:
        logging.exception(f"An error occurred: {e}")


def payment_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Оплатить', callback_data='pay')]  # Correct way
        ]
    )
    return keyboard


@dp.callback_query(lambda c: c.data == 'pay')
async def handle_payment(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("Обработка платежа...")


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
    except Exception as e:
        logging.exception(f"A critical error occurred: {e}")
