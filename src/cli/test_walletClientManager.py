from unittest import TestCase

from cli.wallet_client_manager import WalletClientManager


class TestWalletClientManager(TestCase):
    def test_parse_get_manager_for_contract_response(self):
        response = """
                Disclaimer:
          The  Dune network  is  a  new  blockchain technology.
          Users are  solely responsible  for any risks associated
          with usage of the Dune network.  Users should do their
          own  research to determine  if Dune is the appropriate
          platform for their needs and should apply judgement and
          care in their network interactions.

        dn1KogjUiBYdkBGvUPdRhKrK2cssRqH7eX63 (known as habanoz)
                """
        clientManager = WalletClientManager(None)
        manager = clientManager.parse_get_manager_for_contract_response(response)
        self.assertEqual('dn1KogjUiBYdkBGvUPdRhKrK2cssRqH7eX63', manager)

    def test_parse_client_list_known_contracts_response(self):
        response = """
                Disclaimer:
          The  Dune  network  is  a  new  blockchain technology.
          Users are  solely responsible  for any risks associated
          with usage of the Dune network.  Users should do their
          own  research to determine  if Dune is the appropriate
          platform for their needs and should apply judgement and
          care in their network interactions.

        newcontr: KT1XqEHigP5XumZy9i76QyVd6u93VD4HTqJK
        habanoz: dn1cUpC874bfrF1VDcFbuBwNZ951hdtQQgVg
        mainnetme: dn1WaAD9jDpGmAFwxN2SVBkYo3NnuGR9Ep5G
                """
        clientManager = WalletClientManager(None)
        dict = clientManager.parse_list_known_contracts_response(response)

        self.assertTrue(dict['newcontr'] == 'KT1XqEHigP5XumZy9i76QyVd6u93VD4HTqJK')
        self.assertTrue(dict['habanoz'] == 'dn1cUpC874bfrF1VDcFbuBwNZ951hdtQQgVg')
        self.assertTrue(dict['mainnetme'] == 'dn1WaAD9jDpGmAFwxN2SVBkYo3NnuGR9Ep5G')

    def test_parse_list_known_addresses_response(self):
        response = """
                        Disclaimer:
                  The  Dune  network  is  a  new  blockchain technology.
                  Users are  solely responsible  for any risks associated
                  with usage of the Dune network.  Users should do their
                  own  research to determine  if Dune is the appropriate
                  platform for their needs and should apply judgement and
                  care in their network interactions.

                mainpay: tz1aZoFH2pd3V9UEq5psqVokVBYkt7YSi1ow
                habanoz: dn1cUpC874bfrF1VDcFbuBwNZ951hdtQQgVg (unencrypted sk known)
                mainnetme: dn1WaAD9jDpGmAFwxN2SVBkYo3NnuGR9Ep5G (tcp sk known)
                zeronetme: dn1J3zyiNUUH98wvzeLEzXTKPCpkwaf7YYkb (unencrypted sk not known)
                baker: tz1XXXXXXXX (unix sk known)
                        """

        clientManager = WalletClientManager(None)
        dict = clientManager.parse_list_known_addresses_response(response)

        habanoz = dict['dn1cUpC874bfrF1VDcFbuBwNZ951hdtQQgVg']

        self.assertEqual(habanoz['alias'], 'habanoz')
        self.assertEqual(habanoz['sk'], True)

        mainnetme = dict['dn1WaAD9jDpGmAFwxN2SVBkYo3NnuGR9Ep5G']

        self.assertEqual(mainnetme['alias'], 'mainnetme')
        self.assertEqual(mainnetme['sk'], True)

        zeronetme = dict['dn1J3zyiNUUH98wvzeLEzXTKPCpkwaf7YYkb']

        self.assertEqual(zeronetme['alias'], 'zeronetme')
        self.assertEqual(zeronetme['sk'], False)


        mainpay = dict['tz1aZoFH2pd3V9UEq5psqVokVBYkt7YSi1ow']

        self.assertEqual(mainpay['alias'], 'mainpay')
        self.assertEqual(mainpay['sk'], False)

        baker = dict['tz1XXXXXXXX']
        self.assertEqual(baker['alias'], 'baker')
        self.assertEqual(baker['sk'], True)
