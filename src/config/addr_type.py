from enum import Enum


class AddrType(Enum):
    KT = 1
    DN = 2
    KTALS = 3
    DNALS = 4,

    @staticmethod
    def to_string(obj):
        self = obj
        if self.value==1:
            return 'KT'
        if self.value == 2:
            return 'DN'
        if self.value == 3:
            return 'KTALS'
        if self.value == 4:
            return 'DNALS'
