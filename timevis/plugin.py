import pandas as pd
from .models import (Experiment, Layout, Factor, Level, Plate, Channel,
                     Measure, session)
plugins = {}


class PluginMeta(type):

    def __init__(cls, name, bases, clsdict):
        type.__init__(cls, name, bases, clsdict)
        if name in plugins:
            raise ValueError("Class {} already registered!".format(name))
        elif name == 'Plugin':
            pass
        else:
            plugins[name] = cls


class Plugin(object):
    __metaclass__ = PluginMeta

    @property
    def experiment(self):
        """
        Returns
        -------
        ret: pandas.DataFrame
            A data frame with columns: id, name, user, well
        """
        query = session.query(Experiment)
        ret = pd.read_sql(query.statement, query.session.bind)
        return ret

    @property
    def layout(self):
        """
        Returns
        -------
        ret: pandas.DataFrame
            A data frame with columns: eid, lid, fid, pid, layout, factor, well,
            level
        """
        query = session.query(Factor.id_experiment.label('eid'),
                              Layout.id.label('lid'),
                              Factor.id.label('fid'),
                              Plate.id.label('pid'),
                              Layout.name.label('layout'),
                              Factor.name.label('factor'),
                              Level.well, Level.level).\
            join(Level, Level.id_factor == Factor.id).\
            join(Layout, Layout.id == Level.id_layout).\
            join(Plate, Plate.id_layout == Layout.id)
        ret = pd.read_sql(query.statement, query.session.bind)
        return ret

    @property
    def plate(self):
        """
        Returns
        -------
        ret: pandas.DataFrame
            A data frame with columns: pid, cid, channel, well, time, value
        """
        query = session.query(Plate.id.label('pid'), Channel.id.label('cid'),
                              Channel.name.label('channel'), Measure.well,
                              Measure.time, Measure.measure).\
            join(Channel, Channel.id == Measure.id_channel).\
            join(Measure, Measure.id_plate == Plate.id)
        ret = pd.read_sql(query.statement, query.session.bind)
        return ret
