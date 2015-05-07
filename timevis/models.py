import os.path
from sqlalchemy import ForeignKey, Column, Integer, String, Float, Time
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.engine import Engine
from sqlalchemy import event


# Enable sqlite foreign key support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Create Base, Session and engine
Base = declarative_base()
db_path = os.path.join(os.path.dirname(__file__), 'db', 'timevis.db')
engine = create_engine('sqlite:///{}'.format(db_path))
Session = sessionmaker(bind=engine)


class Experiment(Base):
    """Experiment table contains information describing experiments
    """

    __tablename__ = 'experiments'

    id = Column(Integer, primary_key=True)

    # Experiment name, must be unique
    name = Column(String(255), nullable=False, unique=True)

    # Names of users, comma separated
    user = Column(String(255))

    # Well number, either 96 or 384
    well = Column(Integer, nullable=False)

    # Date of measurement
    # data = Column(Date)

    def __repr__(self):
        return "<Experiment({}, {})>".format(self.name, self.well)


class Factor(Base):
    """Factor table contains information describing factors (independent
    variables)
    """
    __tablename__ = 'factors'

    id = Column(Integer, primary_key=True)

    # Name of factor, usually a controlled condition, like dose
    name = Column(String(255), nullable=False)

    # Type of factor, either 'Category', 'Integer', or 'Decimal'
    type = Column(String(8), nullable=False)

    # Foreign key
    id_experiment = Column(Integer, ForeignKey('experiments.id',
                                               onupdate="CASCADE",
                                               ondelete="CASCADE"))

    # Relationship, a factor record must have an associate experiment record
    experiment = relationship("Experiment",
                              backref=backref('factors', order_by=id))

    def __repr__(self):
        return "<Factor({})>".format(self.name)


class Channel(Base):
    """Channel tables contains information describing measurement
    """
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    # Foreign key
    id_experiment = Column(Integer, ForeignKey('experiments.id',
                                               onupdate="CASCADE",
                                               ondelete="CASCADE"))

    # Channel must have an associate experiment
    experiment = relationship("Experiment",
                              backref=backref('channels', order_by=id))

    def __repr__(self):
        return "<Channel({})>".format(self.name)


class Layout(Base):
    """Layout table describing unique plate setup
    """
    __tablename__ = 'layouts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Foreign key
    id_experiment = Column(Integer, ForeignKey('experiments.id',
                                               onupdate="CASCADE"))

    # Relationship
    layouts = relationship("Experiment",
                           backref=backref('layouts', order_by=id))

    def __repr__(self):
        return "<Layout({})>".format(self.name)


class Plate(Base):
    """Plate table describe invidual plate
    """
    __tablename__ = 'plates'

    id = Column(Integer, primary_key=True)

    # Foreign key
    id_layout = Column(Integer, ForeignKey('layouts.id', onupdate="CASCADE"))

    # Relationship
    plates = relationship("Layout", backref=backref('plates', order_by=id))

    def __repr__(self):
        return "<Plate({})>".format(self.id)


class Level(Base):
    """A table contains all factor levels for different layouts
    """
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)

    # Well name, eg, "A01" or "C04"
    well = Column(String(3), nullable=False)

    # Level of the specific factor, which is indicated by id_factor
    level = Column(String(255))

    # Foreign keys
    id_layout = Column(Integer, ForeignKey('layouts.id',
                                           onupdate="CASCADE",
                                           ondelete="CASCADE"))
    id_factor = Column(Integer, ForeignKey('factors.id',
                                           onupdate="CASCADE",
                                           ondelete="CASCADE"))

    # Associated layout and factor
    layout = relationship("Layout", backref=backref('levels', order_by=id))
    factor = relationship("Factor", backref=backref('levels', order_by=id))


class Value(Base):
    """A table contains all time series data
    """
    __tablename__ = 'values'

    id = Column(Integer, primary_key=True)

    # Well name, eg, "A01" or "C04"
    well = Column(String(3), nullable=False)

    # Time of measurement
    time = Column(Time, nullable=False)

    # Value of measurement
    value = Column(Float, nullable=False)

    id_plate = Column(Integer, ForeignKey('plates.id',
                                          onupdate="CASCADE",
                                          ondelete="CASCADE"))
    id_channel = Column(Integer, ForeignKey('channels.id',
                                            onupdate="CASCADE",
                                            ondelete="CASCADE"))

    # Relationships
    plate = relationship("Plate", backref=backref('values', order_by=id))
    channel = relationship("Channel", backref=backref('values', order_by=id))
