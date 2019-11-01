from cli.cmd_manager import CommandManager
from exception.client import ClientException
from util.client_utils import get_node_rpc_addr


class SimpleClientManager:
    def __init__(self, client_path, verbose=None) -> None:
        super().__init__()
        self.verbose = verbose
        self.client_path = client_path
        self.cmd_manager = CommandManager(verbose)

    def send_request(self, cmd, verbose_override=None, timeout=None):
        rpc_addr = get_node_rpc_addr ()
        whole_cmd = self.client_path + rpc_addr + cmd
        return self.cmd_manager.execute(whole_cmd, verbose_override, timeout=timeout)

    def sign(self, bytes, key_name, verbose_override=None):
        result, response = self.send_request(" sign bytes 0x03{} for {}".format(bytes, key_name), verbose_override=verbose_override)

        if not result:
            raise ClientException("Error at signing: '{}'".format(response))

        for line in response.splitlines():
            if "Signature" in line:
                return line.replace("Signature:","").strip()

        raise ClientException("Signature not found in response '{}'. Signed with key '{}'".format(response, key_name))