import datetime
from dataclasses import dataclass


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
