from unittest import TestCase

from cli.wallet_client_manager import WalletClientManager
from config.addr_type import AddrType
from config.yaml_baking_conf_parser import BakingYamlConfParser
from dunscan.dunscan_block_api import DunScanBlockApiImpl
from dunscan.dunscan_mirror_selection_helper import DunScanMirrorSelector

network={'NAME': 'MAINNET'}
mainnet_public_node_url = "https://rpc.tzbeta.net/"

class TestYamlAppConfParser(TestCase):
    def test_validate(self):

        data_fine = """
        version : 1.0
        baking_address : dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x
        payment_address : dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x
        founders_map : {'KT2Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5,'KT3Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5}
        owners_map : {'KT2Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5,'KT3Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5}
        service_fee : 4.53
        """

        managers = {'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x',
                    'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x'}
        contr_dict_by_alias = {}
        addr_dict_by_pkh = {
            "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x": {"pkh": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x", "originated": False,
                                                     "alias": "main1", "sk": True, "revealed" : True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"},
            "KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj": {"pkh": "KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj", "originated": True,
                                                     "alias": "kt1", "sk": True, "revealed" : True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"}
        }

        wallet_client_manager = WalletClientManager(client_path=None, addr_dict_by_pkh=addr_dict_by_pkh, contr_dict_by_alias=contr_dict_by_alias, managers=managers)

        mirror_selector = DunScanMirrorSelector(network)
        mirror_selector.initialize()
        block_api = DunScanBlockApiImpl(network, mirror_selector)
        cnf_prsr = BakingYamlConfParser(data_fine, wallet_client_manager, provider_factory=None, network_config=network,node_url=mainnet_public_node_url,block_api=block_api)


        cnf_prsr.parse()
        cnf_prsr.validate()

        self.assertEqual(cnf_prsr.get_conf_obj_attr('baking_address'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('payment_address'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_pkh'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_manager'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_type'), AddrType.TZ)
        self.assertEqual(0, cnf_prsr.get_conf_obj_attr('min_delegation_amt'))

    def test_validate_no_founders_map(self):
        data_no_founders = """
        version : 1.0
        baking_address : dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x
        payment_address : dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x
        owners_map : {'KT2Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5,'KT3Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5}
        service_fee : 4.5
        """

        managers_map = {'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x'}


        contr_dict_by_alias = {}
        addr_dict_by_pkh = {
            "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x": {"pkh": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x", "originated": False,
                                                     "alias": "main1", "sk": True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"}}

        wallet_client_manager = WalletClientManager(client_path=None, addr_dict_by_pkh=addr_dict_by_pkh,
                                                    contr_dict_by_alias=contr_dict_by_alias, managers=managers_map)

        mirror_selector = DunScanMirrorSelector(network)
        mirror_selector.initialize()
        block_api = DunScanBlockApiImpl(network, mirror_selector)
        cnf_prsr = BakingYamlConfParser(data_no_founders, wallet_client_manager, provider_factory=None, network_config=network,
                                        node_url=mainnet_public_node_url, block_api=block_api)

        cnf_prsr.parse()
        cnf_prsr.validate()

        self.assertEqual(cnf_prsr.get_conf_obj_attr('baking_address'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('payment_address'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_pkh'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_manager'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_type'), AddrType.TZ)
        self.assertEqual(cnf_prsr.get_conf_obj_attr('founders_map'), dict())
        self.assertEqual(cnf_prsr.get_conf_obj_attr('specials_map'), dict())
        self.assertEqual(cnf_prsr.get_conf_obj_attr('supporters_set'), set())
        self.assertEqual(0, cnf_prsr.get_conf_obj_attr('min_delegation_amt'))

    def test_validate_pymnt_alias(self):
        data_no_founders = """
        version : 1.0
        baking_address : dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x
        payment_address : ktPay
        owners_map : {'KT2Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5,'KT3Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj':0.5}
        service_fee : 4.5
        min_delegation_amt : 100
        """

        managers_map = {'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x',
                        'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x'}

        contr_dict_by_alias = {'ktPay': 'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj'}
        addr_dict_by_pkh = {
            "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x": {"pkh": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x", "originated": False,
                                                     "alias": "tz1", "sk": True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"},
            "KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj": {"pkh": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x", "originated": False,
                                                     "alias": "ktPay", "sk": True, "revealed":True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"}
        }

        wallet_client_manager = WalletClientManager(client_path=None, addr_dict_by_pkh=addr_dict_by_pkh, contr_dict_by_alias=contr_dict_by_alias, managers=managers_map)

        mirror_selector = DunScanMirrorSelector(network)
        mirror_selector.initialize()
        block_api = DunScanBlockApiImpl(network, mirror_selector)
        cnf_prsr = BakingYamlConfParser(data_no_founders, wallet_client_manager, provider_factory=None, network_config=network, node_url=mainnet_public_node_url, block_api=block_api)

        cnf_prsr.parse()
        cnf_prsr.validate()

        self.assertEqual(cnf_prsr.get_conf_obj_attr('baking_address'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('payment_address'), 'ktPay')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_pkh'), 'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_manager'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_type'), AddrType.KTALS)

        self.assertEqual(cnf_prsr.get_conf_obj_attr('founders_map'), dict())
        self.assertEqual(cnf_prsr.get_conf_obj_attr('specials_map'), dict())
        self.assertEqual(cnf_prsr.get_conf_obj_attr('supporters_set'), set())

        self.assertEqual(100, cnf_prsr.get_conf_obj_attr('min_delegation_amt'))

    def test_validate_empty(self):
        data_fine = """
        version : 1.0
        baking_address : dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x
        payment_address : KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj
        service_fee : 4.5
        founders_map : {}
        owners_map : {}
        specials_map : {}
        supporters_set : {}
        min_delegation_amt : 0
        """


        managers = {'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x',
                    'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj': 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x'}

        contr_dict_by_alias = {}
        addr_dict_by_pkh = {
            "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x": {"pkh": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x", "originated": False,
                                                     "alias": "main1", "sk": True, "revealed" : True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"},

            "KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj": {"pkh": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x", "originated": False,
                                                     "alias": "ktPay", "sk": True, "revealed":True,
                                                     "manager": "dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x"}
        }

        wallet_client_manager = WalletClientManager(client_path=None, addr_dict_by_pkh=addr_dict_by_pkh,
                                                    contr_dict_by_alias=contr_dict_by_alias, managers=managers)

        mirror_selector = DunScanMirrorSelector(network)
        mirror_selector.initialize()
        block_api = DunScanBlockApiImpl(network, mirror_selector)
        cnf_prsr = BakingYamlConfParser(data_fine, wallet_client_manager, provider_factory=None,
                                        network_config=network, node_url=mainnet_public_node_url, block_api=block_api)


        cnf_prsr.parse()
        cnf_prsr.validate()

        self.assertEqual(cnf_prsr.get_conf_obj_attr('baking_address'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('payment_address'), 'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_pkh'), 'KT1Z1tMai15JWUWeN2PKL9faXXVPMuWamzJj')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_manager'), 'dn1VWnJRnF3vsa3tkYp3PqoCbV1eBRc5vJ2x')
        self.assertEqual(cnf_prsr.get_conf_obj_attr('__payment_address_type'), AddrType.KT)
        self.assertEqual(0, cnf_prsr.get_conf_obj_attr('min_delegation_amt'))
        self.assertEqual(cnf_prsr.get_conf_obj_attr('supporters_set'), set())
