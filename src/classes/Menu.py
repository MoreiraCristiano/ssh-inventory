from art import tprint
from InquirerPy import inquirer
from .Commands import Commands
from .InventoryHandle import InventoryHandle
from InquirerPy.validator import EmptyInputValidator


class Menu:
    """
    Description: Render and handle user options
    """

    inventory = InventoryHandle()
    commander = Commands()
    screens = {'collections': 'Collections', 'main_menu': 'Main Menu'}

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
        try:
            choice = inquirer.select(
                message='Choose an option:',
                choices=['Add new host', 'Collections', 'Exit'],
            ).execute()

            match choice:
                case 'Add new host':
                    self.add_new_host()
                case 'Collections':
                    self.collections()
                case 'Exit':
                    self.exit()
            return choice
        except KeyboardInterrupt:
            self.exit()
            return 0

    def exit(self):
        """
        Description:
        Parameters:
        Return: Default 0
        """
        try:
            confirm = inquirer.confirm(message='Exit:').execute()
            if confirm:
                print('Bye')
            else:
                self.main_menu()
                return 0
        except KeyboardInterrupt:
            print('Bye')
            return 0

    def add_new_host(self):
        """
        Description: Render steps to add a new host to the database and confirm
        Params:
        Return: 0 if success
        """
        try:
            conn_name = inquirer.text(
                message="Connection name:", validate=EmptyInputValidator()
            ).execute()

            user = inquirer.text(message="Username:", validate=EmptyInputValidator()).execute()

            ip = inquirer.text(message="IP:", validate=EmptyInputValidator()).execute()

            collection = inquirer.text(
                message="Collection:", validate=EmptyInputValidator()
            ).execute()

            confirm = inquirer.confirm(message="Confirm:").execute()

            if confirm:
                try:
                    self.commander.add_new_host(conn_name, user, ip, collection)
                except Exception:
                    print('Name already exists')
                    self.main_menu()
                self.main_menu()
            else:
                choice = inquirer.select(
                    message='What do you want to do:', choices=['Back to main menu', 'Add new host']
                ).execute()

                if choice == 'Back to main menu':
                    self.main_menu()
                elif choice == 'Add new host':
                    self.add_new_host()
            return 0
        except KeyboardInterrupt:
            self.back_to_screen(self.screens['main_menu'])

    def collections(self):
        """
        Description: Instantiates the InventoryHandle class, retrieves the names of all collections, and presents a menu 
         with the names of the collections.
        Params:
        Return: The option choosed (Should be a collection name) or -1 if has no collection in database
        """
        try:
            try:
                collections = sorted(self.inventory.get_distinct_collections_name())
                collections.append('Back')

                collection_choice = inquirer.select(
                    message='Choose a collection:', choices=collections
                ).execute()

                if collection_choice == 'Back':
                    self.back_to_screen(self.screens['main_menu'])
                    return collection_choice

                self.hosts_by_collection(collection_choice)

                return collection_choice
            except Exception:
                print('[-] None collections found')
                self.main_menu()
                return -1
        except KeyboardInterrupt:
            self.back_to_screen(self.screens['main_menu'])

    def hosts_by_collection(self, collection):
        """
        Description: This function receive a collection and get all hosts under then
        Parameters: collection: The queried collection
        Return: The host choosed by user
        """
        try:
            hosts = self.inventory.get_hosts_by_collection(collection)
            choices = [host.conn_name for host in hosts]
            choices.append('Back')

            host_choice = inquirer.select(message='Choose a host:', choices=choices).execute()

            if host_choice == 'Back':
                self.back_to_screen(self.screens['collections'])
                return host_choice

            if hosts != -1:
                for host in hosts:
                    if host.conn_name == host_choice:
                        self.host_actions(host)
                        return host_choice
            else:
                return -1
        except KeyboardInterrupt:
            self.back_to_screen(self.screens['collections'])

    def back_to_screen(self, screen):
        """
        Description: This function receive a screen and return to this
        Parameters: Screen name
        Return: Default 0
        """

        match screen:
            case 'Collections':
                self.collections()
            case 'Main Menu':
                self.main_menu()

        return 0

    def host_actions(self, host):
        """
        Description: Handle choice to host, connect or delete
        Parameters:
        Return: 0 if success or -1 if fails
        """
        choice = inquirer.select(message='Choose a host:', choices=['Connect', 'Delete']).execute()

        match choice:
            case 'Connect':
                self.connect_to_host(host)
            case 'Delete':
                confirm = inquirer.confirm(f'Delete {host.conn_name}:').execute()

                if confirm:
                    self.inventory.remove_host(host)
                    self.back_to_screen(self.screens['collections'])
                else:
                    self.back_to_screen(self.screens['collections'])

        return 0

    def connect_to_host(self, host):
        """
        Description: Call a command class to connect to a host ssh via
        Parameters: Host object
        Return: 0 if success or -1 if fails
        """
        try:
            self.commander.connect_to_host(host.user, host.ip)
            self.main_menu(logo=True)
        except Exception:
            return -1

        return 0
