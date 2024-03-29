import datetime as dt
from models.gender import Gender
from models.treatment import (
    Birth,
    Bovalto1,
    Dehorn,
    Restall,
    Sell,
    Bovalto2,
    Ringworm1,
    Ringworm2,
)


class Calf:
    # Define birthday as a class variable
    _BIRTHDAY: dt.date
    _GENDER: Gender
    _EAR_TAG: int
    _DEHORNING_REQUIRED: bool
    _TO_SELL: bool
    _TREATMENTS: list[
        Birth | Bovalto1 | Dehorn | Restall | Sell | Bovalto2 | Ringworm1 | Ringworm2
    ]
    birth: Birth
    bovalto_1: Bovalto1
    dehorn: Dehorn | None
    restall: Restall

    @property
    def birthday(self) -> dt.date:
        return self._BIRTHDAY

    @property
    def dehorning_required(self) -> bool:
        return self._DEHORNING_REQUIRED

    @property
    def gender(self):
        return self._GENDER

    @property
    def ear_tag(self):
        return self._EAR_TAG

    @property
    def treatments(self):
        return self._TREATMENTS

    @property
    def calf_type(self):
        return self.__class__.__name__.lower().replace("calf", "")

    def __lt__(self, other):
        return self.birthday < other.birthday

    def __gt__(self, other):
        return self.birthday > other.birthday

    def __eq__(self, other):
        return self.birthday == other.birthday

    def __le__(self, other):
        return self.birthday <= other.birthday

    def __ge__(self, other):
        return self.birthday >= other.birthday

    def __init__(
        self,
        birthday: dt.date | str,
        gender: Gender,
        ear_tag: int,
        dehorning_required: bool,
    ):
        if isinstance(birthday, str):
            birthday = dt.datetime.strptime(birthday, "%Y-%m-%d")
            birthday = birthday.date()

        self._BIRTHDAY = birthday
        self._GENDER = gender
        self._EAR_TAG = ear_tag
        self._DEHORNING_REQUIRED = dehorning_required

        self.birth = Birth(self.birthday)

    def change_ear_tag(self, new_ear_tag: int):
        self._EAR_TAG = new_ear_tag

    def edit_gender(self, gender: Gender):
        self._GENDER = gender

    def edit_dehorn(self, date: dt.date):
        self.dehorn.update(date)
        self.restall = Restall(self.dehorn)

    def set_dehorn(self, dehorn: Dehorn):
        self.dehorn = dehorn
        self.restall = Restall(self.dehorn)

    def reset_dehorn(self, date: dt.date, dehorning_required: bool):
        self._DEHORNING_REQUIRED = dehorning_required
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None

        if self.dehorn is not None and self.dehorn.expected_date != date:
            self.dehorn.update(date)

        self.restall = Restall(self.dehorn or self.bovalto_1)

    def delete_dehorn(self):
        self._DEHORNING_REQUIRED = False
        self.dehorn = None
        self.restall = Restall(self.bovalto_1)

    def print_treatment_dates(self):
        for treatment in self.treatments:
            print(f"{treatment.display_name} on {treatment.expected_date}")


class FatteningCalf(Calf):
    def __init__(
        self,
        birthday: dt.date | str,
        gender: Gender,
        ear_tag: int,
        dehorning_required: bool,
    ):
        super().__init__(birthday, gender, ear_tag, dehorning_required)
        self.bovalto_1 = Bovalto1(self.birth)
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None
        self.restall = Restall(self.dehorn or self.bovalto_1)
        self.sell = Sell(self.birth)

        self.__update_treatments()

    def __repr__(self):
        return f"FatteningCalf({self.ear_tag})"

    def __str__(self):
        printed_string = f"FatteningCalf({self.ear_tag})\n"
        printed_string += f"{self.birth}\n"
        for treatment in self.treatments:
            printed_string += f"{treatment}\n"

        return printed_string

    def as_tuple(
        self,
    ) -> tuple[
        int,
        str,
        dt.date,
        str,
        bool,
        dt.date,
        dt.date | None,
        dt.date,
        dt.date,
        None,
        None,
        None,
    ]:
        return (
            self.ear_tag,
            self.calf_type,
            self.birthday,
            str(self.gender),
            self.dehorning_required,
            self.bovalto_1.get_date(),
            self.dehorn.get_date() if self.dehorn else None,
            self.restall.get_date(),
            self.sell.get_date(),
            None,
            None,
            None,
        )

    def reset(
        self,
        birth: Birth,
        bovalto1: Bovalto1,
        dehorn: Dehorn | None,
        restall: Restall,
        sell: Sell,
    ):
        self.birth = birth
        self.bovalto_1 = bovalto1

        if dehorn is None:
            self._DEHORNING_REQUIRED = False
        self.dehorn = dehorn

        self.restall = restall
        self.sell = sell

        self.__update_treatments()

    def __update_treatments(self):
        self._TREATMENTS = [self.bovalto_1, self.dehorn, self.restall, self.sell]

    def edit_birth(self, date: dt.date):
        self.birth.update(date)
        self.bovalto_1 = Bovalto1(self.birth)
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None
        self.restall = Restall(self.dehorn or self.bovalto_1)
        self.sell = Sell(self.birth)
        self.__update_treatments()

    def edit_bovalto1(self, date: dt.date):
        self.bovalto_1.update(date)
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None
        self.restall = Restall(self.dehorn or self.bovalto_1)
        self.__update_treatments()

    def edit_dehorn(self, date: dt.date):
        super().edit_dehorn(date)
        self.__update_treatments()

    def set_dehorn(self, dehorn: Dehorn):
        super().set_dehorn(dehorn)
        self.__update_treatments()

    def reset_dehorn(self, date: dt.date, dehorning_required: bool):
        super().reset_dehorn(date, dehorning_required)
        self.__update_treatments()

    def delete_dehorn(self):
        super().delete_dehorn()
        self.__update_treatments()

    def edit_restall(self, date: dt.date):
        self.restall.update(date)
        self.__update_treatments()

    def edit_sell(self, date: dt.date):
        self.sell.update(date)
        self.__update_treatments()


class BreedingCalf(Calf):
    def __init__(
        self,
        birthday: dt.date | str,
        gender: Gender,
        ear_tag: int,
        dehorning_required: bool,
    ):
        super().__init__(birthday, gender, ear_tag, dehorning_required)

        self.bovalto_1 = Bovalto1(self.birth)
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None
        self.restall = Restall(self.dehorn or self.bovalto_1)
        self.bovalto_2 = Bovalto2(self.bovalto_1)
        self.ringworm_1 = Ringworm1(self.bovalto_2)
        self.ringworm_2 = Ringworm2(self.ringworm_1)
        self.__update_treatments()

    def __repr__(self):
        return f"BreedingCalf({self.ear_tag})"

    def __str__(self):
        printed_string = f"BreedingCalf({self.ear_tag})\n"
        printed_string += f"{self.birth}\n"
        for treatment in self.treatments:
            printed_string += f"{treatment}\n"

        return printed_string

    def __update_treatments(self):
        self._TREATMENTS = [
            self.bovalto_1,
            self.dehorn,
            self.restall,
            self.bovalto_2,
            self.ringworm_1,
            self.ringworm_2,
        ]

    def as_tuple(
        self,
    ) -> tuple[
        int,
        str,
        dt.date,
        str,
        bool,
        dt.date,
        dt.date | None,
        dt.date,
        None,
        dt.date,
        dt.date | None,
        dt.date | None,
    ]:
        return (
            self.ear_tag,
            self.calf_type,
            self.birthday,
            str(self.gender),
            self.dehorning_required,
            self.bovalto_1.get_date(),
            self.dehorn.get_date() if self.dehorn else None,
            self.restall.get_date(),
            None,
            self.bovalto_2.get_date(),
            self.ringworm_1.get_date() if self.ringworm_1 else None,
            self.ringworm_2.get_date() if self.ringworm_2 else None,
        )

    def reset(
        self,
        birth: Birth,
        bovalto1: Bovalto1,
        dehorn: Dehorn | None,
        restall: Restall,
        bovalto2: Bovalto2,
        ringworm1: Ringworm1 | None,
        ringworm2: Ringworm2 | None,
    ):
        self.birth = birth
        self.bovalto_1 = bovalto1

        if dehorn is None:
            self._DEHORNING_REQUIRED = False
        self.dehorn = dehorn

        self.restall = restall
        self.bovalto_2 = bovalto2
        self.ringworm_1 = ringworm1
        self.ringworm_2 = ringworm2

        self.__update_treatments()

    def edit_birth(self, date: dt.date):
        self.birth.update(date)
        self.bovalto_1 = Bovalto1(self.birth)
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None
        self.restall = Restall(self.dehorn or self.bovalto_1)
        self.bovalto_2 = Bovalto2(self.bovalto_1)
        self.ringworm_1 = Ringworm1(self.bovalto_2)
        self.ringworm_2 = Ringworm2(self.ringworm_1)
        self.__update_treatments()

    def edit_bovalto1(self, date: dt.date):
        self.bovalto_1.update(date)
        self.dehorn = Dehorn(self.bovalto_1) if self.dehorning_required else None
        self.restall = Restall(self.dehorn or self.bovalto_1)
        self.bovalto_2 = Bovalto2(self.bovalto_1)
        self.ringworm_1 = Ringworm1(self.bovalto_2)
        self.ringworm_2 = Ringworm2(self.ringworm_1)
        self.__update_treatments()

    def edit_dehorn(self, date: dt.date):
        super().edit_dehorn(date)
        self.__update_treatments()

    def set_dehorn(self, dehorn: Dehorn):
        super().set_dehorn(dehorn)
        self.__update_treatments()

    def reset_dehorn(self, date: dt.date, dehorning_required: bool):
        super().reset_dehorn(date, dehorning_required)
        self.__update_treatments()

    def delete_dehorn(self):
        super().delete_dehorn()
        self.__update_treatments()

    def edit_restall(self, date: dt.date):
        self.restall.update(date)
        self.__update_treatments()

    def edit_bovalto2(self, date: dt.date):
        self.bovalto_2.update(date)

        self.ringworm_1 = Ringworm1(self.bovalto_2)
        self.ringworm_2 = Ringworm2(self.ringworm_1)
        self.__update_treatments()

    def edit_ringworm1(self, date: dt.date):
        if self.ringworm_1 is None:
            self.ringworm_1 = Ringworm1(self.bovalto_2)

        self.ringworm_1.update(date)

        self.ringworm_2 = Ringworm2(self.ringworm_1)
        self.__update_treatments()

    def set_ringworm1(self, ringworm1: Ringworm1):
        """
            Set the ringworm treatments based on the Ringworm1 treatment
        :param ringworm1: New Ringworm1 treatment or the date of the new Ringworm1 treatment
        :return: None
        """
        self.ringworm_1 = ringworm1
        self.ringworm_2 = Ringworm2(self.ringworm_1)

        self.__update_treatments()

    def recalc_ringworm(self, bovalto2: Bovalto2):
        """
            Reset the ringworm treatments based on the Bovalto2 treatment
        :param bovalto2: Bovalto 2 treatment used as base
        :return: None
        """
        self.ringworm_1 = Ringworm1(bovalto2)
        self.ringworm_2 = Ringworm2(self.ringworm_1)

        self.__update_treatments()

    def edit_ringworm2(self, date: dt.date):
        self.ringworm_2.update(date)

        self.__update_treatments()

    def delete_ringworm1(self):
        self.ringworm_1 = None

    def delete_ringworm2(self):
        self.ringworm_2 = None

    def delete_ringworm(self):
        self.delete_ringworm1()
        self.delete_ringworm2()
        self.__update_treatments()
