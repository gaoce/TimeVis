from timevis.models import session
import pandas as pd
from timevis.models import (Experiment, Layout, Factor, Level, Plate, Channel,
                            Value)
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
            A data frame with columns: eid, lid, fid, pid, layout_name,
            factor_name, well, level
        """
        query = session.query(Factor.id_experiment.label('eid'),
                              Layout.id.label('lid'),
                              Factor.id.label('fid'),
                              Plate.id.label('pid'),
                              Layout.name.label('layout_name'),
                              Factor.name.label('factor_name'),
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
            A data frame with columns: pid, cid, channel_name, well, time, value
        """
        query = session.query(Plate.id.label('pid'), Channel.id.label('cid'),
                              Channel.name.label('channel_name'), Value.well,
                              Value.time, Value.value).\
            join(Channel, Channel.id == Value.id_channel).\
            join(Value, Value.id_plate == Plate.id)
        ret = pd.read_sql(query.statement, query.session.bind)
        return ret
