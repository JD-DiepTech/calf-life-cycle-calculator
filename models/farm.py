from datetime import date

from models.calf import FatteningCalf, BreedingCalf
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
from typing import Type, Union, List, Tuple
import datetime as dt


class Farm:
    fattening_calves: list[FatteningCalf]
    breeding_calves: list[BreedingCalf]

    def __init__(self):
        self.fattening_calves = []
        self.breeding_calves = []

    def __sizeof__(self):
        return len(self.fattening_calves) + len(self.breeding_calves)

    def __len__(self):
        return len(self.fattening_calves) + len(self.breeding_calves)

    def __str__(self):
        return f"Farm with {len(self.fattening_calves)} fattening calves and {len(self.breeding_calves)} breeding calves"

    def __repr__(self):
        return f"Farm({self.fattening_calves}, {self.breeding_calves})"

    @property
    def size(self):
        return len(self.fattening_calves) + len(self.breeding_calves)

    def add_calves(
        self, calves: list[FatteningCalf | BreedingCalf], set_ringworm: bool = True
    ):
        for calf in calves:
            self.add_calf(calf, set_ringworm)

    def add_calf(self, calf: FatteningCalf | BreedingCalf, set_ringworm: bool = True):
        # Ear tags must be unique
        if calf.ear_tag in self.get_ear_tags():
            raise Exception(f"Ear tag {calf.ear_tag} already exists")

        if isinstance(calf, FatteningCalf):
            self.__add_fattening_calf(calf)
        elif isinstance(calf, BreedingCalf):
            self.__add_breeding_calf(calf, set_ringworm)
        else:
            raise Exception(
                f"Calf[{calf.ear_tag}] must be either FatteningCalf or BreedingCalf"
            )

    def __add_fattening_calf(self, calf: FatteningCalf):
        # Ear tags must be unique
        if calf.ear_tag in self.get_ear_tags():
            raise Exception(f"Ear tag {calf.ear_tag} already exists")

        self.fattening_calves.append(calf)

    def __add_breeding_calf(self, calf: BreedingCalf, set_ringworm: bool = True):
        # Ear tags must be unique
        if calf.ear_tag in self.get_ear_tags():
            raise Exception(f"Ear tag {calf.ear_tag} already exists")

        self.breeding_calves.append(calf)
        if set_ringworm:
            self.set_ringworm()

    def change_ear_tag(self, old_ear_tag: int, new_ear_tag: int):
        calf = self.get_calf(old_ear_tag)
        calf.change_ear_tag(new_ear_tag)

    def edit_calf(
        self,
        ear_tag: int,
        treatment_type: Type[
            Union[
                Birth
                | Bovalto1
                | Dehorn
                | Restall
                | Sell
                | Bovalto2
                | Ringworm1
                | Ringworm2
            ]
        ],
        date: dt.date,
        dehorning_required: bool,
    ):
        calf = self.get_calf(ear_tag)

        if treatment_type == Birth:
            calf.edit_birth(date)
        elif treatment_type == Bovalto1:
            calf.edit_bovalto1(date)
        elif treatment_type == Dehorn:
            if not calf.dehorning_required and dehorning_required:
                # Currently not dehorned, but dehorning is required
                # Create a dehorning
                calf.reset_dehorn(date, dehorning_required)
            elif calf.dehorning_required and not dehorning_required:
                # Currently dehorned, but dehorning is not required
                # Delete the dehorning
                calf.delete_dehorn()
            elif calf.dehorning_required and dehorning_required:
                # Currently dehorned, and dehorning is required
                # Just change the date
                calf.edit_dehorn(date)
            elif not calf.dehorning_required and not dehorning_required:
                # Currently not dehorned, and dehorning is not required
                # Just go on, nothing to do
                pass
        elif treatment_type == Restall:
            calf.edit_restall(date)

        if isinstance(calf, FatteningCalf):
            if treatment_type == Sell:
                calf.edit_sell(date)
        else:
            if treatment_type == Bovalto2:
                calf.edit_bovalto2(date)
            elif treatment_type == Ringworm1:
                calf.edit_ringworm1(date)
            elif treatment_type == Ringworm2:
                calf.edit_ringworm2(date)

        self.set_ringworm()

    def get_fattening_calf(self, ear_tag: int) -> FatteningCalf:
        for calf in self.fattening_calves:
            if calf.ear_tag == ear_tag:
                return calf
        raise Exception(f"Fattening calf with ear tag {ear_tag} not found")

    def get_breeding_calf(self, ear_tag: int) -> BreedingCalf:
        for calf in self.breeding_calves:
            if calf.ear_tag == ear_tag:
                return calf
        raise Exception(f"Breeding calf with ear tag {ear_tag} not found")

    def get_calf(self, ear_tag: int) -> FatteningCalf | BreedingCalf | None:
        try:
            return self.get_fattening_calf(ear_tag)
        except Exception:
            try:
                return self.get_breeding_calf(ear_tag)
            except Exception:
                print(f"Calf with ear tag {ear_tag} not found")
                return None

    def get_calves(self) -> list[FatteningCalf | BreedingCalf]:
        return self.fattening_calves + self.breeding_calves

    def get_calves_as_tuple(
        self,
    ) -> list[
        tuple[
            int, str, date, str, bool, date, date | None, date, date, None, None, None
        ]
        | tuple[
            int,
            str,
            date,
            str,
            bool,
            date,
            date | None,
            date,
            None,
            date,
            date | None,
            date | None,
        ]
    ]:
        calves = []
        for calf in self.get_calves():
            calves.append(calf.as_tuple())
        return calves

    def get_ear_tags(self) -> list[int]:
        return [calf.ear_tag for calf in self.get_calves()]

    def delete_calf(self, ear_tag: int, set_ringworm: bool = True):
        self.breeding_calves = list(
            filter(lambda x: x.ear_tag != ear_tag, self.breeding_calves)
        )
        self.fattening_calves = list(
            filter(lambda x: x.ear_tag != ear_tag, self.fattening_calves)
        )

        if set_ringworm:
            self.set_ringworm()

    def set_ringworm(self):
        self.breeding_calves.sort(key=lambda calf: calf.birth.expected_date)

        i = 1
        ear_tag_slice = []
        ear_tag_slices = []
        for j in range(len(self.breeding_calves)):
            # Create slices of at least five calves
            cur = self.breeding_calves[j]
            cur_expected_ringworm1 = Ringworm1(cur.bovalto_2)

            if j != len(self.breeding_calves) - 1:
                next_ = self.breeding_calves[j + 1]
                next_expected_ringworm1 = Ringworm1(next_.bovalto_2)
                if (
                    cur_expected_ringworm1.get_week()
                    == next_expected_ringworm1.get_week()
                    or i < 5
                ):
                    #
                    ear_tag_slice.append(cur.ear_tag)
                    i += 1
                else:
                    ear_tag_slice.append(cur.ear_tag)
                    ear_tag_slices.append(ear_tag_slice)
                    ear_tag_slice = []
                    i = 1
            else:
                # Last calf to be sorted
                ear_tag_slice.append(cur.ear_tag)
                ear_tag_slices.append(ear_tag_slice)

        for ear_tags_list in ear_tag_slices:
            print(f"Ear tags in this week: {ear_tags_list}")
            if len(ear_tags_list) >= 5:
                max_bovalto2_breeding_calf = max(
                    (self.get_breeding_calf(ear_tag) for ear_tag in ear_tags_list),
                    key=lambda calf: calf.bovalto_2,
                    default=None,
                )

                for calf in self.breeding_calves:
                    if calf.ear_tag in ear_tags_list:
                        calf.recalc_ringworm(max_bovalto2_breeding_calf.bovalto_2)

                print(
                    f"The maximum Bovalto2 date among the selected ear tags is: {max_bovalto2_breeding_calf.bovalto_2}"
                )

            else:
                print("There are less than five calves in this week.")
                for calf in self.breeding_calves:
                    if calf.ear_tag in ear_tags_list:
                        calf.delete_ringworm()

    def get_jobs_in_week(self, calendar_week: int) -> list[tuple[int, str, dt.date]]:
        jobs = []
        for calf in self.breeding_calves:
            for treatment in calf.treatments:
                if treatment is not None and treatment.get_week() == calendar_week:
                    jobs.append(
                        (
                            calf.ear_tag,
                            treatment.display_name,
                            treatment.expected_date,
                        )
                    )

        for calf in self.fattening_calves:
            for treatment in calf.treatments:
                if treatment is not None and treatment.get_week() == calendar_week:
                    jobs.append(
                        (
                            calf.ear_tag,
                            treatment.display_name,
                            treatment.expected_date,
                        )
                    )

        return jobs

    def get_max_breeding_calf_ear_tag(self):
        # There might be some calves with ear tags starting with 99 (falsly tagged)
        filtered_tags = [
            int(calf.ear_tag)
            for calf in self.breeding_calves
            if not str(calf.ear_tag).startswith("99")
        ]
        return max(filtered_tags, default=0)

    def get_max_fattening_calf_ear_tag(self):
        return max(
            (calf.ear_tag for calf in self.fattening_calves),
            default=0,
        )

    def delete_calves(self, ear_tags: list[int]):
        for ear_tag in ear_tags:
            self.delete_calf(ear_tag, set_ringworm=False)

        self.set_ringworm()
