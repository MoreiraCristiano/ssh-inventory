import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.Host import Host, Base
from sqlalchemy import select
from art import text2art, tprint
from InquirerPy import inquirer


engine = create_engine('sqlite:///db_ssh.sqlite3', echo=True)
Base.metadata.create_all(engine)


class InventoryHandle:
    def __init__(self):
        pass

    def insert_new_host(self, conn_name, user, ip, collection):
        """
        Description:
        Parameters:
        Return:
        """
        with Session(engine) as session:
            new_host = Host(conn_name=conn_name, user=user, ip=ip, collection=collection)
            session.add(new_host)
            session.commit()

        return 0

    def remove_host(self, conn_name):
        """
        Description:
        Parameters:
        Return:
        """
        return 0

    def get_all_hosts(self):
        """
        Description: Obtain all hosts from database
        Params:
        Return: Default 0
        """
        session = Session(engine)
        stmt = select(Host)
        for name in session.scalars(stmt):
            print(name)
        return 0

    def get_hosts_by_collection(self, collection):
        """
        Description: Obtain hosts filtering by collection
        Params: The collection name
        Return: Default 0
        """
        session = Session(engine)
        stmt = select(Host).where(Host.collection.in_([collection]))
        for name in session.scalars(stmt):
            print(name)
        return 0

    def get_distinct_collections_name(self):
        """
        Description: This function must return distinct collections name from db (NEEDS REFACTOR)
        Params:
        Return: List with all collection name
        """
        session = Session(engine)
        stmt = select(Host.collection)
        distinct_collections = set(session.scalars(stmt))

        return list(distinct_collections)


class Menu:
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


class Commands:
    """
    Essa classe se refere ao "enter" do usuario
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
        os.system(f'pwsh ssh_conn.ps1 "{ssh_session}"')

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


if __name__ == '__main__':
    menu = Menu()
    menu.main_menu(logo=True)
