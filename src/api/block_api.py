from abc import ABC, abstractmethod
from math import floor


class BlockApi(ABC):
    def __init__(self, nw):
        super(BlockApi, self).__init__()
        self.nw = nw

    @abstractmethod
    def get_current_level(self, verbose=False):
        pass

    @abstractmethod
    def get_current_cycle(self):
        pass

    @abstractmethod
    def get_next_cycle_first_level(self, current_cycle, verbose=False):
        pass

    @abstractmethod
    def get_revelation(self, pkh, verbose=False):
        pass