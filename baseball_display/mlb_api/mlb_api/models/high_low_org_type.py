from enum import Enum


class HighLowOrgType(str, Enum):
    DIVISION = "DIVISION"
    LEAGUE = "LEAGUE"
    PLAYER = "PLAYER"
    SPORT = "SPORT"
    TEAM = "TEAM"

    def __str__(self) -> str:
        return str(self.value)
