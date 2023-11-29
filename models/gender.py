from enum import Enum


class Gender(Enum):
    Male = "m"
    Female = "w"

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, gender_str):
        for gender in cls:
            if gender.value == gender_str.lower():
                return gender
        raise ValueError("Invalid gender string")
