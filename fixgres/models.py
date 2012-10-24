from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://localhost/fixgres')
Base = declarative_base(engine)

Session = sessionmaker(bind=engine)

class Email(Base):
    __tablename__ = 'emails'
    __table_args__ = {'autoload': True}
