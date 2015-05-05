import os.path
from sqlalchemy import ForeignKey, Column, Integer, String, Float, Time
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


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
    name = Column(String, nullable=False, unique=True)

    # Names of users, comma separated
    user = Column(String)

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
    name = Column(String(50), nullable=False)

    # Type of factor, either 'Category', 'Integer', or 'Decimal'
    type = Column(String, nullable=False)

    # Foreign key
    id_Experiment = Column(Integer, ForeignKey('experiments.id'))

    # Relationship
    experiments = relationship("Experiment",
                               backref=backref('factors', order_by=id))

    def __repr__(self):
        return "<Factor({})>".format(self.name)


class Channel(Base):
    """Channel tables contains information describing measurement
    """
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Foreign key
    id_Experiment = Column(Integer, ForeignKey('experiments.id'))

    # Relationship
    channels = relationship("Experiment",
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
    id_Experiment = Column(Integer, ForeignKey('experiments.id'))

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
    id_Layout = Column(Integer, ForeignKey('layouts.id'))

    # Relationship
    plates = relationship("Layout", backref=backref('plates', order_by=id))

    def __repr__(self):
        return "<Plate({})>".format(self.id)


class Level(Base):
    """A table contains all factor levels
    """
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)

    # Name of the well
    well = Column(String, nullable=False)

    # Level of the specific factor, which is indicated by id_Factor
    level = Column(String)

    # Foreign keys
    id_Layout = Column(Integer, ForeignKey('layouts.id'))
    id_Plate = Column(Integer, ForeignKey('plates.id'))
    id_Factor = Column(Integer, ForeignKey('factors.id'))

    # Relationships
    # layout_levels = relationship("Layout",
    #                              backref=backref('levels', order_by=id))
    # plate_levels = relationship("Plate",
    #                             backref=backref('levels', order_by=id))
    # factor_levels = relationship("Factor",
    #                              backref=backref('levels', order_by=id))


class Value(Base):
    """A table contains all time series data
    """
    __tablename__ = 'values'

    id = Column(Integer, primary_key=True)

    # Well name
    well = Column(String, nullable=False)

    # Time of measurement
    time = Column(Time, nullable=False)

    # Value of measurement
    value = Column(Float, nullable=False)

    id_Plate = Column(Integer, ForeignKey('plates.id'))
    id_Channel = Column(Integer, ForeignKey('channels.id'))

    # Relationships
    # plate_values = relationship("Plate",
    #                             backref=backref('values', order_by=id))
    # channel_values = relationship("Channel",
    #                               backref=backref('values', order_by=id))
