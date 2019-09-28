import requests

from api.block_api import BlockApi
from exception.dunscan import DunScanException
from log_config import main_logger

logger = main_logger

HEAD_API = {'MAINNET': {'HEAD_API_URL': 'https://api.dunscan.io/v3/head'},
            'TESTNET': {'HEAD_API_URL': 'http://api%MIRROR%.testnet.dunscan.io/v3/head'},
            'DEVNET': {'HEAD_API_URL': 'http://api.devnet.dunscan.io/v3/head'}
            }

REVELATION_API = {'MAINNET': {'HEAD_API_URL': 'https://api.dunscan.io/v3/operations/%PKH%?type=Reveal'},
                  'TESTNET': {'HEAD_API_URL': 'https://api%MIRROR%.testnet.dunscan.io/v3/operations/%PKH%?type=Reveal'},
                  'DEVNET': {'HEAD_API_URL': 'https://api.devnet.dunscan.io/v3/operations/%PKH%?type=Reveal'}
                  }

LEVEL_API = {'MAINNET': {'HEAD_API_URL': 'https://api.dunscan.io/v1/level/%LEVEL%'},
            'TESTNET': {'HEAD_API_URL': 'http://api%MIRROR%.testnet.dunscan.io/v1/level/%LEVEL%'},
            'DEVNET': {'HEAD_API_URL': 'http://api.devnet.dunscan.io/v1/level/%LEVEL%'}
            }


class DunScanBlockApiImpl(BlockApi):

    def __init__(self, nw, mirror_selector):
        super(DunScanBlockApiImpl, self).__init__(nw)

        self.head_api = HEAD_API[nw['NAME']]
        if self.head_api is None:
            raise Exception("Unknown network {}".format(nw))

        self.revelation_api = REVELATION_API[nw['NAME']]
        self.level_api = LEVEL_API[nw['NAME']]
        self.mirror_selector = mirror_selector

    def get_current_level(self, verbose=False):
        uri = self.head_api['HEAD_API_URL'].replace("%MIRROR%", str(self.mirror_selector.get_mirror()))

        if verbose:
            logger.debug("Requesting {}".format(uri))

        resp = requests.get(uri, timeout=5)
        if resp.status_code != 200:
            # This means something went wrong.
            self.mirror_selector.validate_mirrors()
            raise DunScanException('GET {} {}'.format(uri, resp.status_code))
        root = resp.json()

        if verbose:
            logger.debug("Response from dunscan is: {}".format(root))

        current_level = int(root["level"])

        return current_level

    def get_current_cycle(self, verbose=False):
        uri = self.head_api['HEAD_API_URL'].replace("%MIRROR%", str(self.mirror_selector.get_mirror()))

        if verbose:
            logger.debug("Requesting {}".format(uri))

        resp = requests.get(uri, timeout=5)
        if resp.status_code != 200:
            # This means something went wrong.
            self.mirror_selector.validate_mirrors()
            raise DunScanException('GET {} {}'.format(uri, resp.status_code))
        root = resp.json()

        if verbose:
            logger.debug("Response from dunscan is: {}".format(root))

        cycle = int(root["cycle"])

        return cycle

    def get_revelation(self, pkh, verbose=False):
        uri = self.revelation_api['HEAD_API_URL'].replace("%MIRROR%", str(self.mirror_selector.get_mirror())).replace("%PKH%", pkh)

        if verbose:
            logger.debug("Requesting {}".format(uri))

        resp = requests.get(uri, timeout=5)
        if resp.status_code != 200:
            # This means something went wrong.
            self.mirror_selector.validate_mirrors()
            raise DunScanException('GET {} {}'.format(uri, resp.status_code))
        root = resp.json()

        if verbose:
            logger.debug("Response from dunscan is: {}".format(root))

        return len(root) > 0

    def get_next_cycle_first_level(self, current_cycle, verbose=False):

        uri = self.head_api['HEAD_API_URL'].replace("%MIRROR%", str(self.mirror_selector.get_mirror()))

        if verbose:
            logger.debug("Requesting {}".format(uri))

        resp = requests.get(uri, timeout=5)
        if resp.status_code != 200:
            # This means something went wrong.
            self.mirror_selector.validate_mirrors()
            raise DunScanException('GET {} {}'.format(uri, resp.status_code))
        root = resp.json()

        if verbose:
            logger.debug("Response from dunscan is: {}".format(root))

        level_hash = root["hash"]

        uri = self.level_api['HEAD_API_URL'].replace("%MIRROR%", str(self.mirror_selector.get_mirror())).replace("%LEVEL%", level_hash)

        if verbose:
            logger.debug("Requesting {}".format(uri))

        resp = requests.get(uri, timeout=5)
        if resp.status_code != 200:
            # This means something went wrong.
            self.mirror_selector.validate_mirrors()
            raise DunScanException('GET {} {}'.format(uri, resp.status_code))
        root = resp.json()

        if verbose:
            logger.debug("Response from dunscan is: {}".format(root))

        cycle_position = int(root["cycle_position"])

        return self.nw['BLOCKS_PER_CYCLE'] - cycle_position