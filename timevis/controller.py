"""Transcations that facilitate interaction between views and models.
"""
from timevis.models import session, commit
from timevis.models import (Experiment, Layout, Channel, Factor, Level, Value,
                            Plate)
from sqlalchemy.orm import aliased
import pandas
from scikits.bootstrap import ci
from numpy import mean


def get_exps():
    """Retrieve experiment records in the database and return them in an array
    of json objects.
    """
    exps_out = []
    # Get Experiment instance and fill in the result dict
    for exp_rec in session.query(Experiment).all():
        exps_out.append(exp_rec)

    # Return a list of experiment json object
    return [exp.json for exp in exp_recs]


def post_exps(exp_jsons):
    """Insert experiment objects into database.

    Parameters
    ----------
    exp_jsons : list
        list of experiment json objs

    Returns
    -------
    list
        list of (uploaded) experiment json objs
    """

    # List of experiment records for committing and output formatting
    exp_recs = []

    # Loop thru input Experiment obj and insert them into db. Create and insert
    # associated Channel and Factor records in the meantime
    for exp_json in exp_jsons:
        # The new experiment obj should have a exp_id of 0
        if str(exp_json['id']) != '0':
            return "New experiment ID should be '0'"

        # New experiment record
        exp_rec = Experiment(name=exp_json['name'], user=exp_json['user'],
                             well=exp_json['well'])

        # Create a Channel object, associate it with exp_rec, it will be
        # inserted when we add exp_rec to Experiment table through cascading
        for cha in exp_json['channels']:
            Channel(name=cha['name'], experiment=exp_rec)

        # Insert new factors
        for fac in exp_json['factors']:
            Factor(name=fac['name'], type=fac['type'], experiment=exp_rec)

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
        eid = json['id']
        # Exp record must exist and be only one
        exp_rec = session.query(Experiment).filter_by(id=eid).one()
        exp_rec.update_exp(json)                 # Update record itsefl
        exp_rec.update_chnls(json['channels'])   # Update associate Channels
        exp_rec.update_facts(json['factors'])    # Update associate Factors
        exp_recs.append(exp_rec)

    # Commit the changes
    commit()

    # Return a list of experiment json object
    return [exp.json for exp in exp_recs]


def construct_layout(layout_rec, eid):
    """Given a layout rec, construct layout obj for output
    """
    layout_out = {"id": layout_rec.id,
                  "name": layout_rec.name,
                  "factors": []}

    for fac_rec in session.query(Factor).filter_by(id_experiment=eid).all():
        fac_out = {"id": fac_rec.id,
                   "name": fac_rec.name,
                   "levels": {}}

        for well, level in session.query(Level.well, Level.level).\
                filter(Level.id_factor == fac_rec.id).\
                filter(Level.id_layout == layout_rec.id).all():
            fac_out['levels'][well] = level

        layout_out['factors'].append(fac_out)

    return layout_out


def get_layouts(eid):
    """
    """
    layouts_out = []
    for layout_rec in session.query(Layout).filter_by(id_experiment=eid).all():
        layout_out = construct_layout(layout_rec, eid)
        layouts_out.append(layout_out)

    return layouts_out


def post_layouts(layouts_in, eid):
    """
    """
    # Get layout id and data, lid should be 0
    layouts_rec = []
    for layout_in in layouts_in:

        # Create a new Layout record
        layout_rec = Layout(name=layout_in['name'], id_experiment=eid)

        # Update level records
        for fac_in in layout_in['factors']:
            # Factor ID
            fid = fac_in['id']
            for well, level in fac_in['levels'].items():
                Level(well=well, level=level, layout=layout_rec, id_factor=fid)

        layouts_rec.append(layout_rec)

    # Commit the changes
    session.add_all(layouts_rec)
    commit()

    # Prepare return value
    layouts_out = []
    for layout_rec in layouts_rec:
        layout_out = construct_layout(layout_rec, eid)
        layouts_out.append(layout_out)

    return layouts_out


def put_layouts(layouts_in):
    """
    """
    layouts_rec = []
    # Get layout id and data
    for layout_in in layouts_in:
        # Got layout obj and modify it
        lid = layout_in['id']
        layout_rec = session.query(Layout).filter_by(id=lid).one()
        layout_rec.name = layout_in['name']

        # Update level records
        # Only update factor provided
        for fac_rec in layout_in['factors']:
            fid = fac_rec['id']
            flvl = fac_rec['levels']
            # levels = []
            # for level in session.query(Level).\
            #         filter(Level.id_layout == lid).\
            #         filter(Level.id_factor == fid).all():
            #     level.level = flvl[level.well]
            try:
                for level in layout_rec.levels:
                    if level.id_factor == fid:
                        level.level = flvl.pop(level.well)
            except KeyError as err:
                return err.message

            for well, lvl in flvl.items():
                Level(well=well, level=lvl, id_factor=fid, layout=layout_rec)

        layouts_rec.append(layout_rec)

    # Commit the changes
    session.add_all(layouts_rec)
    commit()

    # Prepare return value
    layouts_out = []
    for layout_rec in layouts_rec:
        layout_out = construct_layout(layout_rec, layout_rec.id_experiment)
        layouts_out.append(layout_out)

    return layouts_out


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
            cha_out['time'] = [str(t[0]) for t in session.query(Value.time).
                               distinct().order_by(Value.time).all()]
            cha_out['well'] = [val[0] for val in session.query(Value.well).
                               distinct().order_by(Value.well).all()]
            # Current time point
            curr_time = None
            values = None
            for val in session.query(Value).order_by(Value.time, Value.well).\
                    all():
                if curr_time != val.time:
                    curr_time = val.time
                    # Just finish a loop
                    if values is not None:
                        cha_out['value'].append(values)
                    # Reset
                    values = []
                values.append(val.value)

            # Append the last time point
            cha_out['value'].append(values)
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
        plate_rec.delete_values()
        plate_rec.update_chnls(json['channels'])

    commit()

    return jsons


queries = []


def post_time(json):
    """
    """

    # Construct query
    q = session.query(Value.time, Value.value).\
        join(Plate).\
        join(Channel).\
        filter(Channel.id == json['channel'])

    for fac_in in json['factors']:
        Level_a = aliased(Level)
        Factor_a = aliased(Factor)
        q = q.join(Level_a, Level_a.well == Value.well).\
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
        query[fname] = fac_in['levels']

    return query
