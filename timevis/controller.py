"""Transcations that facilitate interaction between views and models.
"""
from .models import session, commit
from .models import (Experiment, Layout, Channel, Factor, Level, Measure,
                     Plate)
from sqlalchemy.orm import aliased
import pandas
from scikits.bootstrap import ci
from numpy import mean


def get_exps():
    """Retrieve experiment records in the database and return them in an array
    of json objects.
    """
    # Get Experiment instance and fill in the result dict
    exp_recs = session.query(Experiment).all()

    # Return a list of experiment json object
    return [exp.json for exp in exp_recs]


def post_exps(jsons):
    """Insert experiment objects into database.

    Parameters
    ----------
    jsons : list
        list of experiment json objs

    Returns
    -------
    list
        list of (uploaded) experiment json objs
    """

    # List of experiment records for committing and output formatting
    exp_recs = []

    # Loop thru input Experiment obj and insert them into db.
    for json in jsons:
        # The new experiment obj should have a exp_id of 0
        if str(json['id']) != '0':
            return "New experiment ID should be '0'"
        # Create new Experiment record and update it
        exp_rec = Experiment()
        exp_rec.update_exp(json)
        exp_recs.append(exp_rec)

    # Commit the changes
    session.add_all(exp_recs)
    commit()

    # Return a list of experiment json object
    return [exp.json for exp in exp_recs]


def put_exps(jsons):
    """Update Experiment records according input experiment objs

    Parameters
    ----------
    jsons : list
        input list of experiment objs

    Returns
    -------
    list
        list of (updated) experiment json objs
    """
    exp_recs = []
    for json in jsons:
        # Exp record must exist and be only one
        exp_rec = session.query(Experiment).filter_by(id=json['id']).one()
        # Update record
        exp_rec.update_exp(json)
        exp_recs.append(exp_rec)

    # Commit the changes
    commit()

    # Return a list of experiment json object
    return [exp.json for exp in exp_recs]


def get_layouts(eid):
    """Retrieve Layout records given Experiment ID

    Returns
    list
        a list of Layout json objs
    """
    layout_recs = session.query(Layout).filter_by(id_experiment=eid).all()

    return [layout.json for layout in layout_recs]


def post_layouts(jsons, eid):
    """
    """
    # Get layout id and data, lid should be 0
    layout_recs = []
    for json in jsons:
        # Create a new Layout record
        layout_rec = Layout()
        layout_rec.update_layout(json, eid)
        layout_recs.append(layout_rec)

    # Commit the changes
    session.add_all(layout_recs)
    commit()

    # Return a list of Layout json objs
    return [layout.json for layout in layout_recs]


def put_layouts(jsons, eid):
    """
    """
    layout_recs = []
    # Get layout id and data
    for json in jsons:
        # Got layout obj and modify it
        layout_rec = session.query(Layout).filter_by(id=json['id']).one()
        layout_rec.update_layout(json, eid)
        layout_recs.append(layout_rec)

    # Commit the changes
    commit()

    # Return a list of Layout json objs
    return [layout.json for layout in layout_recs]


def get_plates(lid):
    """
    """
    plates = []

    # Layout obj
    layout_rec = session.query(Layout).filter_by(id=lid).first()

    # Plate inside layout
    for plate_rec in layout_rec.plates:
        plate_out = {"id": plate_rec.id, "channels": []}

        for cha_rec in layout_rec.experiment.channels:
            cha_out = {"id": cha_rec.id, "name": cha_rec.name, "value": []}
            cha_out['time'] = [str(t[0]) for t in session.query(Measure.time).
                               distinct().order_by(Measure.time).all()]
            cha_out['well'] = [val[0] for val in session.query(Measure.well).
                               distinct().order_by(Measure.well).all()]
            # Current time point
            curr_time = None
            measures = None
            for measure in session.query(Measure).\
                    order_by(Measure.time, Measure.well).all():
                if curr_time != measure.time:
                    curr_time = measure.time
                    # Just finish a loop
                    if measures is not None:
                        cha_out['value'].append(measures)
                    # Reset
                    measures = []
                measures.append(measure.measure)

            # Append the last time point
            cha_out['value'].append(measures)
            plate_out['channels'].append(cha_out)

        plates.append(plate_out)

    return plates


def post_plates(jsons, lid):
    """
    """
    # For commit purpose
    plates_rec = []

    # Get layout id and data
    for json in jsons:
        plate_rec = Plate(id_layout=lid)
        plate_rec.update_chnls(json['channels'])
        plates_rec.append(plate_rec)

    session.add_all(plates_rec)
    commit()

    # The plate id is now available, update json obj with it
    for idx, plate_rec in enumerate(plates_rec):
        jsons[idx]['id'] = plate_rec.id

    return jsons


def put_plates(jsons):
    """Update all channels data on a plate

    Parameters
    ----------
    jsons: list
        list of plate json objects

    Returns
    -------
    list of (updated) plate json objects
    """
    # Get layout id and data
    for json in jsons:
        # Plate id
        pid = json['id']
        plate_rec = session.query(Plate).filter_by(id=pid).first()
        plate_rec.delete_measures()
        plate_rec.update_chnls(json['channels'])

    commit()

    return jsons


queries = []


def post_time(json):
    """
    """

    # Construct query
    q = session.query(Measure.time, Measure.measure).\
        join(Plate).\
        join(Channel).\
        filter(Channel.id == json['channel'])

    for fac_in in json['factors']:
        Level_a = aliased(Level)
        Factor_a = aliased(Factor)
        q = q.join(Level_a, Level_a.well == Measure.well).\
            join(Factor_a, Factor_a.id == Level_a.id_factor).\
            filter(Level_a.level.in_(fac_in['levels'])).\
            filter(Factor_a.id == fac_in['id'])

    # Get data frame
    df = pandas.read_sql(q.statement, q.session.bind)

    def cc(x):
        cis = ci(x)
        return (cis[1] - cis[0])/2

    # Record query
    res = {'id': len(queries), 'query': get_ret_query(json), 'result': []}
    queries.append(json)

    df_g = df.groupby(['time']).aggregate([mean, cc])
    for row in df_g.iterrows():
        res['result'].append({
            "value": row[1][0],
            "time": str(row[0]),
            "l": row[1][0] - row[1][1],
            "u": row[1][0] + row[1][1]})

    return res


def get_ret_query(json):
    """Construct a dict to display query nicely, i.e.,
    Original query format::

        {
          "experiment": eid,
          "channel"   : cid,
          "factors"   :
          [
            {
              "id"    : fid,
              "levels": flvl,
            },
            ...
          ]
        }

    Returned query format::
        {
          "experiment": ename,
          "channel"   : cname,
          "factor1"   : levels,
          ...
        }

    """
    # Construct returning query
    query = {}
    query['Experiment'] = session.query(Experiment.name).\
        filter_by(id=json['experiment']).one()[0]
    query['Channel'] = session.query(Channel.name).\
        filter_by(id=json['channel']).one()[0]

    for fac_in in json['factors']:
        fname = session.query(Factor.name).filter_by(id=fac_in['id']).one()[0]
        query[fname] = " | ".join(fac_in['levels'])

    return query
