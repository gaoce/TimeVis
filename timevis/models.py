from . import app
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import ForeignKey, Column, Integer, String, Float, Time
from sqlalchemy.orm import relationship, backref


class Experiment(Base):
        __tablename__ = 'experiments'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        user = Column(String)
        well = Column(Integer)

        def __repr__(self):
            return "<Experiment({}, {})>".format(self.name, self.well)


class Factor(Base):
    __tablename__ = 'factors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)

    id_Experiment = Column(Integer, ForeignKey('experiments.id'))

    experiments = relationship("Experiment", backref=backref('factors',
                                                             order_by=id))

    def __repr__(self):
        return "<Factor({})>".format(self.name)


class Layout(Base):
    __tablename__ = 'layouts'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    id_Experiment = Column(Integer, ForeignKey('experiments.id'))

    layouts = relationship("Experiment", backref=backref('layouts',
                                                         order_by=id))

    def __repr__(self):
        return "<Layout({})>".format(self.name)


class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    id_Experiment = Column(Integer, ForeignKey('experiments.id'))

    channels = relationship("Experiment", backref=backref('channels',
                                                          order_by=id))

    def __repr__(self):
        return "<Channel({})>".format(self.name)


class Plate(Base):
    __tablename__ = 'plates'

    id = Column(Integer, primary_key=True)

    id_Layout = Column(Integer, ForeignKey('layouts.id'))

    plates = relationship("Layout", backref=backref('plates', order_by=id))

    def __repr__(self):
        return "<Plate({})>".format(self.id)


class Level(Base):
    """A table contains all factor levels
    """
    __tablename__ = 'levels'

    id = Column(Integer, primary_key=True)
    levels = Column(String)

    id_Layout = Column(Integer, ForeignKey('layouts.id'))
    id_Plate = Column(Integer, ForeignKey('plates.id'))
    id_Factor = Column(Integer, ForeignKey('factors.id'))

    layout_levels = relationship("Layout", backref=backref('levels',
                                                           order_by=id))

    plate_levels = relationship("Plate", backref=backref('levels',
                                                         order_by=id))

    factor_levels = relationship("Factor", backref=backref('levels',
                                                           order_by=id))


class Value(Base):
    """A table contains all time series data
    """
    __tablename__ = 'values'

    id = Column(Integer, primary_key=True)
    well = Column(String)
    time = Column(Time)
    value = Column(Float)

    id_Plate = Column(Integer, ForeignKey('plates.id'))
    id_Channel = Column(Integer, ForeignKey('channels.id'))

    plate_values = relationship("Plate", backref=backref('values', order_by=id))

    channel_values = relationship("Channel", backref=backref('values',
                                                             order_by=id))

print(app)
