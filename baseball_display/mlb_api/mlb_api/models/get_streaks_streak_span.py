from enum import Enum


class GetStreaksStreakSpan(str, Enum):
    CAREER = "career"
    CURRENTSTREAK = "currentStreak"
    CURRENTSTREAKINSEASON = "currentStreakInSeason"
    NOTABLE = "notable"
    NOTABLEINSEASON = "notableInSeason"
    SEASON = "season"

    def __str__(self) -> str:
        return str(self.value)
