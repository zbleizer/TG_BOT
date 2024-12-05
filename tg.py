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
        """Calculates compatibility percentage based on biorhythm differences."""

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


def get_digit_sum(number: int) -> int:
    return sum(int(digit) for digit in str(number))


def zero_fill(number: int, width: int = 2) -> str:
    return str(number).zfill(width)


@dataclasses.dataclass
class PythagorasSquare:
    birthdate: datetime.date

    def __post_init__(self) -> None:
        self.string_birthdate = self.birthdate.strftime("%d%m%Y")
        self.digit_rows = self.get_digit_rows()
        self.character = Sector(
            digit=1,
            title="Характер",
            value=self.get_sector_value(1),
        )
        self.energy = Sector(
            digit=2,
            title="Энергия",
            value=self.get_sector_value(2),
        )
        self.interest = Sector(
            digit=3,
            title="Интерес",
            value=self.get_sector_value(3),
        )
        self.health = Sector(
            digit=4,
            title="Здоровье",
            value=self.get_sector_value(4),
        )
        self.logic = Sector(
            digit=5,
            title="Логика",
            value=self.get_sector_value(5),
        )
        self.labour = Sector(
            digit=6,
            title="Труд",
            value=self.get_sector_value(6),
        )
        self.luck = Sector(
            digit=7,
            title="Удача",
            value=self.get_sector_value(7),
        )
        self.duty = Sector(
            digit=8,
            title="Долг",
            value=self.get_sector_value(8),
        )
        self.memory = Sector(
            digit=9,
            title="Память",
            value=self.get_sector_value(9),
        )

        self.self_assessment = Sector(
            digit=None,
            title="Самооценка",
            value=self.get_additional_sector_value(
                [self.character, self.energy, self.interest],
            ),
        )
        self.life = Sector(
            digit=None,
            title="Быт",
            value=self.get_additional_sector_value(
                [self.health, self.logic, self.labour],
            ),
        )
        self.talent = Sector(
            digit=None,
            title="Талант",
            value=self.get_additional_sector_value([self.luck, self.duty, self.memory]),
        )
        self.goal = Sector(
            digit=None,
            title="Цель",
            value=self.get_additional_sector_value(
                [self.character, self.health, self.luck],
            ),
        )
        self.family = Sector(
            digit=None,
            title="Семья",
            value=self.get_additional_sector_value(
                [self.energy, self.logic, self.duty],
            ),
        )
        self.habits = Sector(
            digit=None,
            title="Привычки",
            value=self.get_additional_sector_value(
                [self.interest, self.labour, self.memory],
            ),
        )
        self.spirit = Sector(
            digit=None,
            title="Дух",
            value=self.get_additional_sector_value(
                [self.character, self.logic, self.memory],
            ),
        )
        self.temperament = Sector(
            digit=None,
            title="Темперамент",
            value=self.get_additional_sector_value(
                [self.interest, self.logic, self.luck],
            ),
        )

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
                list(zero_fill(self.get_first_number()))
                + list(zero_fill(self.get_second_number()))
                + list(zero_fill(self.get_third_number()))
                + list(zero_fill(self.get_fourth_number()))
        )

        return [
            [int(digit) for digit in self.string_birthdate],
            [int(digit) for digit in second_row],
        ]

    def get_sector_value(self, digit: int) -> int:
        value: int = 0
        numbers = self.digit_rows[0] + self.digit_rows[1]
        for d in numbers:
            if d == digit:
                value += 1
        return value

    @staticmethod
    def get_additional_sector_value(base_sectors: list[Sector]) -> int:
        value: int = 0
        for base_sector in base_sectors:
            value += base_sector.value
        return value

    def get_magic_square_printable(self) -> list[list[str]]:
        return [
            [
                self.get_printable_sector_value(self.character),
                self.get_printable_sector_value(self.health),
                self.get_printable_sector_value(self.luck),
            ],
            [
                self.get_printable_sector_value(self.energy),
                self.get_printable_sector_value(self.logic),
                self.get_printable_sector_value(self.duty),
            ],
            [
                self.get_printable_sector_value(self.interest),
                self.get_printable_sector_value(self.labour),
                self.get_printable_sector_value(self.memory),
            ],
        ]

    @staticmethod
    def get_printable_sector_value(sector: Sector) -> str:
        if sector.value == 0:
            return "нет цифр"
        if sector.digit is not None:
            return str(sector.digit) * sector.value
        else:
            return str(sector.value)

    def __repr__(self) -> str:
        return (
            f"Квадрат Пифагора для {self.birthdate.strftime('%d.%m.%Y')}:\n\n"
            f"Характер - {self.get_printable_sector_value(self.character)}\n"
            f"Энергия - {self.get_printable_sector_value(self.energy)}\n"
            f"Интерес - {self.get_printable_sector_value(self.interest)}\n"
            f"Здоровье - {self.get_printable_sector_value(self.health)}\n"
            f"Логика - {self.get_printable_sector_value(self.logic)}\n"
            f"Труд - {self.get_printable_sector_value(self.labour)}\n"
            f"Удача - {self.get_printable_sector_value(self.luck)}\n"
            f"Долг - {self.get_printable_sector_value(self.duty)}\n"
            f"Память - {self.get_printable_sector_value(self.memory)}\n"
            f"Самооценка - {self.get_printable_sector_value(self.self_assessment)}\n"
            f"Быт - {self.get_printable_sector_value(self.life)}\n"
            f"Талант - {self.get_printable_sector_value(self.talent)}\n"
            f"Цель - {self.get_printable_sector_value(self.goal)}\n"
            f"Семья - {self.get_printable_sector_value(self.family)}\n"
            f"Привычки - {self.get_printable_sector_value(self.habits)}\n"
            f"Дух - {self.get_printable_sector_value(self.spirit)}\n"
            f"Темперамент - {self.get_printable_sector_value(self.temperament)}\n"
        )


class Form(StatesGroup):
    waiting_for_birthdate = State()
    waiting_for_first_birthdate = State()
    waiting_for_second_birthdate = State()


with open('TOKEN.txt', 'r') as f:
    token = f.read().strip()

start_router = Router()
bot = Bot(token)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
dp.include_router(start_router)

logging.basicConfig(level=logging.INFO)

button_prediction = KeyboardButton(text="Получить предсказание")
button_compatibility = KeyboardButton(text="Совместимость")
button_help = KeyboardButton(text="Помощь")

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_prediction],
        [button_compatibility],
        [button_help]
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
    if message.text == "Получить предсказание":
        await state.set_state(Form.waiting_for_birthdate)
        await message.answer("Введите свою дату рождения (в формате ДД.ММ.ГГГГ):")

    elif message.text == "Совместимость":
        await state.set_state(Form.waiting_for_first_birthdate)
        await message.answer("Введите первую дату рождения (в формате ДД.ММ.ГГГГ):")

    elif message.text == "Помощь":
        await cmd_help(message)
    else:

        if await state.get_state() == Form.waiting_for_birthdate:
            await handle_birthdate(message, state)

        elif await state.get_state() == Form.waiting_for_first_birthdate:
            await process_first_birthdate(message, state)

        elif await state.get_state() == Form.waiting_for_second_birthdate:
            await process_second_birthdate(message, state)


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
        biorhythm_result = BiorithmCompatibility(birthday1, birthday2)
        pythagoras1 = PythagorasSquare(birthday1)
        pythagoras2 = PythagorasSquare(birthday2)
        biorhythm_str = (f"Physical: {biorhythm_result.physical}\n"
                         f"Emotional: {biorhythm_result.emotional}\n"
                         f"Intelligent: {biorhythm_result.intelligent}\n"
                         f"Heart: {biorhythm_result.heart}\n"
                         f"Creative: {biorhythm_result.creative}\n"
                         f"Intuitive: {biorhythm_result.intuitive}\n"
                         f"Higher: {biorhythm_result.higher}\n"
                         f"Summary: {biorhythm_result.summary}")

        return (
            f"Совместимость между {birthday1.strftime('%d.%m.%Y')} и {birthday2.strftime('%d.%m.%Y')} рассчитана.\n"
            f"Биоритмы:\n{biorhythm_str}\n"
            f"\n{pythagoras1}\n"
            f"\n{pythagoras2}"
        )

    except Exception as e:
        return f"Ошибка при расчете совместимости: {e}"


def validate_date(date_str):
    try:
        date = parse(date_str, dayfirst=True)
        if date > datetime.datetime.now():
            raise ValueError("Future dates are not allowed.")
        return date.date()
    except ValueError as e:
        raise ValueError(f"Invalid date: {e}")


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
