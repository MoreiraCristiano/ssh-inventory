from art import tprint
from InquirerPy import inquirer
from .Commands import Commands
from .InventoryHandle import InventoryHandle


class Menu:
    """
    Descripttion: Render and handle user options
    """

    def __init__(self):
        pass

    def main_menu(self, logo=False):
        """
        Description: Render the main menu
        Params:
        Return: The choosed option
        """
        if logo:
            tprint('SSH-INVENTORY', font='small')

        choice = inquirer.select(
            message='Choose an option:', choices=['Add new host', 'Collections', 'Exit']
        ).execute()

        match choice:
            case 'Add new host':
                self.add_new_host()
            case 'Collections':
                self.collections()
            case 'Exit':
                confirm = inquirer.confirm(message='Exit:').execute()
                if confirm:
                    return choice
                else:
                    self.main_menu()
        return choice

    def add_new_host(self):
        """
        Description: Render steps to add a new host to the database and confirm
        Params:
        Return: 0 if success
        """
        conn_name = inquirer.text(message="Connection name:").execute()
        user = inquirer.text(message="Username:").execute()
        ip = inquirer.text(message="IP:").execute()
        collection = inquirer.text(message="Collection:").execute()

        confirm = inquirer.confirm(message="Confirm:").execute()
        if confirm:
            commander = Commands()
            commander.add_new_host(conn_name, user, ip, collection)
        else:
            choice = inquirer.select(
                message='What do you want to do:', choices=['Back to main menu', 'Add new host']
            ).execute()

            if choice == 'Back to main menu':
                self.main_menu()
            elif choice == 'Add new host':
                self.add_new_host()
        return 0

    def collections(self):
        """
        Description: Instantiates the InventoryHandle class, retrieves the names of all collections, and presents a menu with the names of the collections.
        Params:
        Return: The option choosed (Should be a collection name)
        """
        inventory = InventoryHandle()

        try:
            collections = inventory.get_distinct_collections_name()
            choice = inquirer.select(
                message='Choose a collection:', choices=sorted(collections)
            ).execute()

            return choice
        except Exception:
            print('None collections found')
            self.main_menu()
            return -1
