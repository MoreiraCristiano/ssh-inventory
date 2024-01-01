from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass


class Host(Base):
    __tablename__ = 'hosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    conn_name: Mapped[str] = mapped_column(String(30))
    user: Mapped[str] = mapped_column(String(50))
    ip: Mapped[str] = mapped_column(String(25))
    collection: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f'Host(id={self.id!r}, conn_name={self.conn_name!r}, user={self.user!r}, ip={self.ip!r}, collection={self.collection!r})'
