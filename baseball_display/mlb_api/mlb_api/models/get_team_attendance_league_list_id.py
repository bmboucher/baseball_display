from enum import Enum


class GetTeamAttendanceLeagueListId(str, Enum):
    ABL = "abl"
    BASEBALL_ALL = "baseball_all"
    MILB_ALL = "milb_all"
    MILB_ALL_DOMESTIC = "milb_all_domestic"
    MILB_ALL_NOMEX = "milb_all_nomex"
    MILB_COMPLEX = "milb_complex"
    MILB_DOMCOMP = "milb_domcomp"
    MILB_FULL = "milb_full"
    MILB_INTCOMP = "milb_intcomp"
    MILB_NONCOMP = "milb_noncomp"
    MILB_NONCOMP_NOMEX = "milb_noncomp_nomex"
    MILB_SHORT = "milb_short"
    MLB = "mlb"
    MLB_HIST = "mlb_hist"
    MLB_MILB = "mlb_milb"
    MLB_MILB_HIST = "mlb_milb_hist"
    MLB_MILB_WIN = "mlb_milb_win"
    WIN_ALL = "win_all"
    WIN_CARIBBEAN = "win_caribbean"
    WIN_NOABL = "win_noabl"

    def __str__(self) -> str:
        return str(self.value)
