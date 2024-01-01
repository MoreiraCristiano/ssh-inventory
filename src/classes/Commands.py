from os import system
from .InventoryHandle import InventoryHandle


class Commands:
    """
    Description: This class is a controller when user choose and select an option
    """

    def __init__(self):
        pass

    def connect_to_host(self, user, ip):
        """
        Description: Use a powershell script to run ssh command in CLI
        Parameters: user for ssh connection and ip
        Return: Default 0
        """
        ssh_session = f'ssh {user}@{ip}'
        system(f'pwsh ../shell_scripts/ssh_conn.ps1 "{ssh_session}"')

        return 0

    def add_new_host(self, conn_name, user, ip, collection):
        """
        Description:
        Parameters: Receive all information about the host to add in db
        Return: Default 0
        """
        inventory = InventoryHandle()
        inventory.insert_new_host(conn_name, user, ip, collection)

        return 0
