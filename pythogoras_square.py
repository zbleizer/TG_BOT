import dataclasses
import datetime


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

    def zero_fill(number, width):
        """Pads a number with leading zeros."""
        return str(number).zfill(width)

    def get_digit_sum(number):
        """Calculates the sum of digits of a number."""
        return sum(int(digit) for digit in str(number))

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
        ) # calc pyth square
