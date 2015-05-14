"""Transcations that facilitate interaction between views and models.
"""
from sqlalchemy.exc import SQLAlchemyError

from timevis.models import session
from timevis.models import Experiment, Layout, Channel, Factor, Level


def get_exps():
    """
    """
    exps_out = []
    # Get Experiment instance and fill in the result dict
    for exp_rec in session.query(Experiment).all():
        exps_out.append(construct_exp(exp_rec))

    return exps_out


def insert_exps(exps_in):
    """Insert experiment objects into database.

    Parameters
    ----------
    exps_in : list
        input list of experiment objs

    Returns
    -------
    exps_out: list or str
        output list of experiemnt objs that have just been inserted, if error
        occurs, return error message
    """
    # Experiment objs list to be returned
    exps_out = []

    # Loop thru input Experiment obj and insert them into db. Create and insert
    # associated Channel and Factor records in the meantime
    for exp_in in exps_in:
        # The new experiment obj should have a exp_id of 0
        if str(exp_in['id']) != '0':
            return "New experiment ID should be '0'"

        # New experiment record
        exp_rec = Experiment(name=exp_in['name'], user=exp_in['user'],
                             well=exp_in['well'])

        # Create a Channel object, associate it with exp_rec, it will be
        # inserted when we add exp_rec to Experiment table through cascading
        for cha in exp_in['channels']:
            Channel(name=cha['name'], experiment=exp_rec)

        # Insert new factors
        for fac in exp_in['factors']:
            Factor(name=fac['name'], type=fac['type'], experiment=exp_rec)

        # Commit the changes for experiment, channels and factors
        session.add(exp_rec)
        try:
            session.commit()
        except SQLAlchemyError as err:
            session.rollback()
            return err.message

        # Append the inserted Experiment obj into returning list
        exps_out.append(construct_exp(exp_rec))

    return exps_out


def update_exps(exps_in):
    """Update Experiment records according input experiment objs

    Parameters
    ----------
    exps_in : list
        input list of experiment objs

    Returns
    -------
    exps_out: list or str
        output list of experiemnt objs that have just been inserted, if error
        occurs, return error message
    """
    exps_out = []

    for exp_in in exps_in:
        eid = exp_in['id']
        # Exp record must exist and be only one
        exp_rec = session.query(Experiment).filter_by(id=eid).one()
        exp_rec.name = exp_in['name']
        exp_rec.user = exp_in['user']
        exp_rec.well = exp_in['well']

        # Update channel record in database, delete un-associated channel
        for ch_rec in session.query(Channel).filter_by(id_experiment=eid).all():
            for ch_in in exp_in['channels']:
                if ch_rec.id == ch_in['id']:
                    ch_rec.name = ch_in['name']
                    break

        for f_rec in session.query(Factor).filter_by(id_experiment=eid).all():
            for f_in in exp_in['factors']:
                if f_rec.id == f_in['id']:
                    f_rec.name, f_rec.type = f_in['name'], f_in['type']
                    break
        try:
            session.commit()
        except SQLAlchemyError as err:
            session.rollback()
            return err.message

        exps_out.append(construct_exp(exp_rec))

    return exps_out


def construct_exp(exp_rec):
    """Helper function. Construct experiment obj using an experiment record.

    Parameters
    ----------
    exp_rec : Experiment record
        an experiment record

    Returns
    -------
    ret : dict
        an experiment object
    """
    ret = {"id": exp_rec.id,
           "name": exp_rec.name,
           "user": exp_rec.user,
           "well": exp_rec.well,
           "channels": [{"id": c.id, "name": c.name} for c in exp_rec.channels],
           "factors": [{"id": f.id, "name": f.name, "type": f.type,
                        "levels": uni_lvl(f.id)} for f in exp_rec.factors]}
    return ret


def uni_lvl(fid):
    """Helper function. Get unique levels given a factor ID.
    """
    res = []
    for row in session.query(Level.level).filter_by(id_factor=fid).\
            distinct().all():
        res.append(row[0])
    return res


def get_layouts(eid):
    """
    """

    layouts_out = []
    for layout_rec in session.query(Layout).filter_by(id_experiment=eid).all():
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
    try:
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        return err.message

    for idx, layout in enumerate(layouts_rec):
        # Only Layout id is changed (a new one is given)
        layouts_in[idx]['id'] = layout.id

    return layouts_in


def put_layouts(layouts_in):
    # Get layout id and data
    for layout_in in layouts_in:
        # Got layout obj and modify it
        lid = layout_in['id']
        layout_rec = session.query(Layout).filter_by(id=lid)
        layout_rec.name = layout_in['name']

        # Update level records
        # Only update factor provided
        for fac_rec in layout_in['factors']:
            fid = fac_rec['id']
            flvl = fac_rec['levels']
            # levels = []
            for level in session.query(Level).\
                    filter(Level.id_layout == lid).\
                    filter(Level.id_factor == fid).all():
                level.level = flvl[level.well]

    # Commit the changes
    try:
        session.commit()
    except SQLAlchemyError as err:
        session.rollback()
        return err.message

    return layouts_in
