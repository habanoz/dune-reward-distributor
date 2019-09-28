from abc import ABC, abstractmethod


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
    def get_revelation(self, pkh, verbose=False):
        pass

    @abstractmethod
    def get_current_level_hash(self, verbose=False):
        pass

    @abstractmethod
    def get_current_cycle_position(self, level_hash, verbose=False):
        pass