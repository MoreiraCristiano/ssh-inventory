from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class Base(DeclarativeBase):
    pass


class Host(Base):
    __tablename__ = 'hosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    conn_name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    user: Mapped[str] = mapped_column(String(50), nullable=False)
    ip: Mapped[str] = mapped_column(String(25), nullable=False)
    collection: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'Host(id={self.id!r}, conn_name={self.conn_name!r}, user={self.user!r}, ip={self.ip!r}, collection={self.collection!r})'
