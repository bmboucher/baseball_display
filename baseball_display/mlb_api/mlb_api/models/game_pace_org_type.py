from enum import Enum


class GamePaceOrgType(str, Enum):
    L_LEAGUE = "L- LEAGUE"
    S_SPORT = "S- SPORT"
    T_TEAM = "T- TEAM"

    def __str__(self) -> str:
        return str(self.value)
