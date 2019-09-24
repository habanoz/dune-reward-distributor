from unittest import TestCase

from calc.calculate_phase0 import CalculatePhase0
from dunscan.dunscan_reward_api import DunscanRewardApiImpl
from model import reward_log
from dunscan.dunscan_mirror_selection_helper import DunScanMirrorSelector

BAKING_ADDRESS = "dn1YJhqRgFWHKsaYE1JL8xyCrS8eeqXTusuu"


class TestCalculatePhase0(TestCase):

    def test_calculate(self):
        nw = {"NAME": "TESTNET"}
        mirror_selector = DunScanMirrorSelector(nw)
        mirror_selector.initialize()

        api = DunscanRewardApiImpl(nw, BAKING_ADDRESS, mirror_selector)
        model = api.get_rewards_for_cycle_map(17)

        phase0 = CalculatePhase0(model)
        reward_data, total_rewards = phase0.calculate()

        staking_balance = int(model.delegate_staking_balance)

        # total reward ratio is 1
        self.assertTrue(1.0, sum(r.ratio0 for r in reward_data))

        # check that ratio calculations are correct
        delegators_balances = model.delegator_balance_dict

        # check ratios
        for (address, balance), reward in zip(delegators_balances.items(),reward_data):
            # ratio must be equal to stake/total staking balance
            self.assertEqual(int(balance) / staking_balance, reward.ratio0)

        # last one is owners record
        self.assertTrue(reward_data[-1].type == reward_log.TYPE_OWNERS_PARENT)
