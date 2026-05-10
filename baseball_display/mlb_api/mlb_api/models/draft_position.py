from enum import Enum


class DraftPosition(str, Enum):
    B = "B"
    BR = "BR"
    C = "C"
    CF = "CF"
    CP = "CP"
    DH = "DH"
    IF = "IF"
    LF = "LF"
    LHP = "LHP"
    LHR = "LHR"
    LHS = "LHS"
    OF = "OF"
    P = "P"
    PH = "PH"
    PR = "PR"
    RF = "RF"
    RHP = "RHP"
    RHR = "RHR"
    RHS = "RHS"
    RP = "RP"
    SP = "SP"
    SS = "SS"
    UI = "UI"
    UO = "UO"
    UT = "UT"
    VALUE_2 = "1B"
    VALUE_3 = "2B"
    VALUE_4 = "3B"
    X = "X"

    def __str__(self) -> str:
        return str(self.value)
