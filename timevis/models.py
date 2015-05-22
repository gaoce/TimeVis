import os.path
from sqlalchemy import ForeignKey, Column, Integer, String, Float, Time
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.engine import Engine
from sqlalchemy import event

from datetime import datetime


# Enable sqlite foreign key support
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Create Base, Session and engine
Base = declarative_base()
db_path = os.path.join(os.path.dirname(__file__), 'db', 'timevis.db')
db_url = 'sqlite:///{}'.format(db_path)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


def commit():
    """Commit the changes.
    If error occurs, rollback session and re-throw the exception, which will be
    bubbled up and handled by ``api`` module
    """
    try:
        session.commit()
    except:
        session.rollback()
        raise


class Experiment(Base):
    """Experiment table contains information describing experiments
    Additional attributes:
        factors
        channels
        layouts
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

    @property
    def json(self):
        """Convert a Experiment record to a json object (a dict really)

        Returns
        -------
        ret : dict
            an experiment object
        """
        return {"id": self.id,
                "name": self.name,
                "user": self.user,
                "well": self.well,
                "channels": [{"id": c.id,
                              "name": c.name} for c in self.channels],
                "factors": [{"id": f.id,
                             "name": f.name,
                             "type": f.type,
                             "levels": f.uniq_lvls} for f in self.factors]
                }

    def update_exp(self, json):
        """Update experiment record given experiment json obj

        Parameters:
            json: dict
                an experiment json object
        """
        self.name = json['name']
        self.user = json['user']
        self.well = json['well']
        self.update_facts(json['factors'])
        self.update_chnls(json['channels'])

    def update_chnls(self, chnls):
        """Update Channel records associated with the Experiment record
        Update existing Channel records contained in the input, delete existing
        channels not contained in the input. Add new Channels not in the
        existing.

        Parameters
        ----------
        chnls: list of dict
            a list of Channel json objs
        """
        chs_update = {}  # Channels to be updated
        chs_upload = []  # Newly created channels
        for ch_in in chnls:
            if ch_in['id'] != 0:
                chs_update[ch_in['id']] = ch_in
            else:
                chs_upload.append(ch_in)

        for ch_rec in self.channels:
            cid = ch_rec.id
            if cid in chs_update:
                ch_rec.name = chs_update[cid]['name']
            else:
                # Delete those not included in chs_update
                session.delete(ch_rec)

        for ch_in in chs_upload:
            Channel(name=ch_in['name'], experiment=self)

    def update_facts(self, factors):
        """Update Factor records associated with Experiment record

        Parameters
        ----------
        factors: list of dict
            a list of Factor json objs
        """

        facs_update = {}
        facs_upload = []
        for fac_in in factors:
            if fac_in['id'] != 0:
                facs_update[fac_in['id']] = fac_in
            else:
                facs_upload.append(fac_in)

        for fac_rec in session.query(Factor).filter_by(experiment=self).all():
            fid = fac_rec.id
            if fid in facs_update:
                fac_rec.name = facs_update[fid]['name']
                fac_rec.type = facs_update[fid]['type']
            else:
                session.delete(fac_rec)

        for fac_in in facs_upload:
            Factor(name=fac_in['name'], type=fac_in['type'], experiment=self)

    def __repr__(self):
        return "<Experiment({}, {}, {})>".format(self.id, self.name, self.well)


class Factor(Base):
    """Factor table contains information describing factors (independent
    variables)
    Additional attributes:
        levels
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

    @property
    def uniq_lvls(self):
        res = []
        for row in session.query(Level.level).filter_by(factor=self).\
                distinct().all():
            res.append(row[0])
        return res

    def __repr__(self):
        return "<Factor({}, {})>".format(self.id, self.name)


class Channel(Base):
    """Channel tables contains information describing measurement
    Additional attributes:
        values
    """
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)

    # Channel name
    name = Column(String(255), nullable=False)

    # Foreign key
    id_experiment = Column(Integer, ForeignKey('experiments.id',
                                               onupdate="CASCADE",
                                               ondelete="CASCADE"))

    # Channel must have an associate experiment
    experiment = relationship("Experiment",
                              backref=backref('channels', order_by=id))

    def __repr__(self):
        return "<Channel({}, {})>".format(self.id, self.name)


class Layout(Base):
    """Layout table describing unique plate setup
    Additional attributes:
        plates
        levels
    """
    __tablename__ = 'layouts'
    id = Column(Integer, primary_key=True)

    # Layout name
    name = Column(String, nullable=False)

    # Foreign key
    id_experiment = Column(Integer, ForeignKey('experiments.id',
                                               onupdate="CASCADE"))

    # Relationship
    experiment = relationship("Experiment",
                              backref=backref('layouts', order_by=id))

    @property
    def json(self):
        """Given a layout rec, construct layout obj for output
        """
        json = {"id": self.id, "name": self.name, "factors": []}

        # This can be done by a single layer for loop thru join
        for fact_rec in session.query(Factor).\
                filter_by(experiment=self.experiment).all():
            fact_json = {"id": fact_rec.id, "name": fact_rec.name, "levels": {}}

            for well, level in session.query(Level.well, Level.level).\
                    filter_by(factor=fact_rec).filter_by(layout=self).all():
                fact_json['levels'][well] = level

            json['factors'].append(fact_json)

        return json

    def update_layout(self, json, eid):
        """Update Layout record based on input Layout json object
        """
        self.name = json['name']
        self.id_experiment = eid
        self.update_facts(json['factors'])

    def update_facts(self, factors):
        # Update level records
        # Only update factor provided
        for fact_json in factors:
            fid = fact_json['id']
            flvl = fact_json['levels']
            try:
                for level in self.levels:
                    if level.id_factor == fid:
                        level.level = flvl.pop(level.well)
            except KeyError as err:
                return err.message

            for well, lvl in flvl.items():
                Level(well=well, level=lvl, id_factor=fid, layout=self)

    def __repr__(self):
        return "<Layout({}, {})>".format(self.id, self.name)


class Plate(Base):
    """Plate table describe invidual plate
    Additional attributes:
        values
    """
    __tablename__ = 'plates'
    id = Column(Integer, primary_key=True)

    # Foreign key
    id_layout = Column(Integer, ForeignKey('layouts.id', onupdate="CASCADE"))

    # Relationship
    layout = relationship("Layout", backref=backref('plates', order_by=id))

    def update_chnls(self, chnls):
        """Update Channel records associated with plate
        """
        for chnl in chnls:
            chnl_rec = session.query(Channel).filter_by(id=chnl['id']).first()

            # Data structure
            #        well1 well2 ...
            # time1 [[val1, val2, ... ],
            # time2  [...,            ],
            #        [...,            ],
            # ...    [...,            ]]
            t_fmt = "%H:%M:%S"  # Time string format
            times = [datetime.strptime(t, t_fmt).time() for t in chnl['time']]
            wells = chnl['well']
            vals = chnl['value']
            for time, vals in zip(times, vals):
                for well, val in zip(wells, vals):
                    Value(well=well, time=time, value=val, plate=self,
                          channel=chnl_rec)

    def delete_values(self):
        """Delete all values associated with Plate
        """
        for value in self.values:
            session.delete(value)

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
    level = Column(String(255), nullable=False)

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

    def __repr__(self):
        return "<Level({}\t{}\t{}\t{}\t{})>".format(self.id, self.layout.name,
                                                    self.factor.name, self.well,
                                                    self.level)


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

    def __repr__(self):
        return "<Value({}\t{}\t{}\t{}\t{})>".format(self.id, self.plate.id,
                                                    self.channel.name,
                                                    self.well, self.value)
