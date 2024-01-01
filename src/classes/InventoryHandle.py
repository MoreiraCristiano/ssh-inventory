from sqlalchemy.orm import Session
from sqlalchemy import select
from model.Host import Host, Base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db_ssh.sqlite3', echo=False)
Base.metadata.create_all(engine)


class InventoryHandle:
    def __init__(self):
        pass

    def insert_new_host(self, conn_name, user, ip, collection):
        """
        Description: This function instantiate a new Host class and add to database
        Parameters:conn_name: The name to session, user: SSH user, ip: Host IP, collection: The collection to save
        Return: Default 0
        """
        with Session(engine) as session:
            new_host = Host(conn_name=conn_name, user=user, ip=ip, collection=collection)
            session.add(new_host)
            session.commit()

        return 0

    def remove_host(self, conn_name):
        """
        Description: This function receive the session name and delete from base. Collection too?
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
