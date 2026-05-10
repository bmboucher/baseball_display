from enum import Enum


class GetStreaksStreakType(str, Enum):
    HITTINGSTREAKAWAY = "hittingStreakAway"
    HITTINGSTREAKHOME = "hittingStreakHome"
    HITTINGSTREAKOVERALL = "hittingStreakOverall"
    ONBASEAWAY = "onBaseAway"
    ONBASEHOME = "onBaseHome"
    ONBASEOVERALL = "onBaseOverall"

    def __str__(self) -> str:
        return str(self.value)
