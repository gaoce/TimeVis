from timevis import app
from flask import render_template, request
from flask.ext.restful import Api, Resource, reqparse
from timevis.models import (Experiment, Layout, Factor, Channel, Level, Plate,
                            Value, Session)

from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


class ExperimentEP(Resource):
    """Endpoint for experiment information
    This endpoint mainly deals with Experiment, Channel and Factor tables.
    """
    def get(self):
        # Result
        ret = {"experiment": []}

        # Create query session
        # TODO: session scope and context manager
        s = Session()

        # Get Experiment instance and fill in the result dict
        for e in s.query(Experiment).all():
            ret["experiment"].append(self.construct_exp(e))

        return ret

    def post(self):
        """Create a new experiment:
            1. Create a new record in Experiment table;
            2. Create new records in Channel and Factor tables.
        """
        # Create query session
        s = Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Experiment obj array for return purpose
        experiments = []

        # Insert each experiment obj to table, creating new factors and channels
        for obj in json['experiment']:
            # The new experiment obj should have a exp_id of 0
            if str(obj['id']) != '0':
                return "New experiment ID should be '0'"

            # New experiment record
            e = Experiment(name=obj['name'], user=obj['user'], well=obj['well'])

            # Create a Channel object, associate it with e, it will be inserted
            # when we add e to experiment table through cascading
            for c in obj['channels']:
                Channel(name=c['name'], experiment=e)

            # Insert new factors
            for f in obj['factors']:
                Factor(name=f['name'], type=f['type'], experiment=e)

            # Commit the changes for experiment, channels and factors
            s.add(e)
            # TODO try except
            s.commit()

            experiments.append(self.construct_exp(e))

        # Return the updated experiment obj
        return {"experiment": experiments}

    def put(self):
        """Update experiment information:
            1. Update experiment record;
            3. Add new channel and factor records
        """

        # Create query session
        s = Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Array of experiment obj, return purpose
        experiments = []

        # Get experimen id and data body
        for obj in json['experiment']:
            eid = obj['id']
            # Exp record must exist and be only one
            # TODO try except
            e = s.query(Experiment).filter_by(id=eid).one()
            e.name, e.user, e.well = obj['name'], obj['user'], obj['well']

            # Update channel record in database, delete un-associated channel
            for c in s.query(Channel).filter_by(id_experiment=eid).all():
                # A flag
                found_c = 0
                for ch in obj['channels']:
                    if c.id == ch['id']:
                        c.name = ch['name']
                        found_c = 1
                        # I tried to remove ch from obj['channels'] here, but
                        # considered it too dangerous
                        break
                if found_c == 0:
                    s.delete(c)

            for f in s.query(Factor).filter_by(id_experiment=eid).all():
                # A flag
                found_f = 0
                for fa in obj['factors']:
                    if f.id == fa['id']:
                        f.name, f.type = fa['name'], fa['type']
                        found_f = 1
                        break
                if found_f == 0:
                    s.delete(f)

            # Commit the changes
            # TODO try except
            s.commit()
            experiments.append(self.construct_exp(e))

        # Return the updated experiment obj
        return {"experiment": experiments}

    def construct_exp(self, e):
        """Helper function, construct exp obj using an Experiment record
        """
        ret = {"id": e.id,
               "name": e.name,
               "user": e.user,
               "well": e.well,
               "channels": [{"id": c.id, "name": c.name} for c in e.channels],
               "factors": [{"id": f.id, "name": f.name, "type": f.type}
                           for f in e.factors]}
        return ret


class LayoutEP(Resource):
    """Layout endpoint
    This endpoint mainly query Layout, Factor and Level tables, and modify Level
    and Layout tables
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('eid', type=int, help="experiment id")
        args = parser.parse_args()
        eid = args.eid

        # Create query session
        s = Session()

        # Result
        ret = {"layout": []}

        for l in s.query(Layout).filter_by(id_experiment=eid).all():
            layout_obj = {}
            layout_obj["id"] = l.id
            layout_obj["name"] = l.name
            layout_obj["factors"] = []

            for f in s.query(Factor).filter_by(id_experiment=eid).all():
                fac = {}
                fac['id'] = f.id
                fac['name'] = f.name
                fac['levels'] = {}

                for well, lvl in s.query(Level.well, Level.level).\
                        filter(Level.id_factor == f.id).\
                        filter(Level.id_layout == l.id).all():
                    fac['levels'][well] = lvl

                layout_obj['factors'].append(fac)

            ret["layout"].append(layout_obj)

        return ret

    def post(self):
        """Create a new layout obj:
            1. Create a new record in Layout table
            2. Create new records in Level table
        """
        parser = reqparse.RequestParser()
        parser.add_argument('eid', type=int, help="experiment id")
        args = parser.parse_args()
        eid = args.eid

        # Create query session
        s = Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Get layout id and data, lid should be 0
        layouts = []
        for data in json["layout"]:

            # Create a new Layout record
            l = Layout(name=data['name'], id_experiment=eid)

            # Update level records
            for f in data['factors']:
                # Factor ID
                fid = f['id']
                for well, level in f['levels'].items():
                    Level(well=well, level=level, layout=l, id_factor=fid)

            layouts.append(l)

        # Commit the changes
        s.add_all(layouts)
        s.commit()

        for idx, l in enumerate(layouts):
            # Only Layout id is changed (a new one is given)
            json['layout'][idx]['id'] = l.id

        # Return newly create obj
        return json

    def put(self):
        """Update a layout's name and its levels"""
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Create query session
        s = Session()

        # Get layout id and data
        for data in json["layout"]:
            # Got layout obj and modify it
            lid = data['id']
            l = s.query(Layout).filter_by(id=lid)
            l.name = data['name']

            # Update level records
            # Only update factor provided
            for f in data['factors']:
                fid = f['id']
                flvl = f['levels']
                # levels = []
                for lvl in s.query(Level).\
                        filter(Level.id_layout == lid).\
                        filter(Level.id_factor == fid).all():
                    lvl.level = flvl[lvl.well]

        # Commit the changes
        s.commit()

        # Nothing to change, really
        return json


class PlateEP(Resource):
    """Retrieve, upload and update plate information. This endpoint mainly
    queries Plate, Value tables, and modified Plate, Channel, Value tables
    """
    def get(self):
        # Parse args
        parser = reqparse.RequestParser()
        parser.add_argument('lid', type=int, help="layout id")
        args = parser.parse_args()
        lid = args.lid
        pass

    def post(self):
        """Input new plates"""

        # Parse args
        parser = reqparse.RequestParser()
        parser.add_argument('lid', type=int, help="layout id")
        args = parser.parse_args()
        lid = args.lid

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Create query session
        s = Session()

        # For commit purpose
        plates = []

        # Get layout id and data
        for data in json['plate']:
            p = Plate(id_layout=lid)
            plates.append(p)

            for ch in data['channels']:
                c = s.query(Channel).filter_by(id=ch['id']).first()

                # Parse time
                time_array = [datetime.strptime(t, "%H:%M:%S").time()
                              for t in ch['time']]
                well_array = ch['well']
                for t, val_array in zip(time_array, ch['value']):
                    for well, val in zip(well_array, val_array):
                        Value(well=well, time=t, value=val, plate=p, channel=c)

        s.add_all(plates)
        try:
            s.commit()
        except Exception as e:
            print e
            return 'failed'

        # The plate id is now available, update json obj with it
        for idx, p in enumerate(plates):
            json['plate'][idx]['id'] = p.id
        return json

    def put(self):
        """Update plates data"""
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Create query session
        s = Session()

        # Newly created value
        values = []

        # Get layout id and data
        for data in json['plate']:
            # Plate id
            pid = data['id']
            p = s.query(Plate).filter_by(id=pid).first()

            s.query(Value).filter_by(id_plate=pid).delete()

            for ch in data['channels']:
                c = s.query(Channel).filter_by(id=ch['id']).first()

                # Parse time
                time_array = [datetime.strptime(t, "%H:%M:%S").time()
                              for t in ch['time']]
                well_array = ch['well']
                for t, val_array in zip(time_array, ch['value']):
                    for well, val in zip(well_array, val_array):
                        values.append(Value(well=well, time=t, value=val,
                                            plate=p, channel=c))

        s.add_all(values)
        s.commit()

        # Nothing to change
        return json


class TimeSeriesEP(Resource):
    pass

api = Api(app)
api_root = '/api/v2'
api.add_resource(ExperimentEP, api_root + '/experiment')
api.add_resource(LayoutEP,     api_root + '/layout')
api.add_resource(PlateEP,      api_root + '/plate')
api.add_resource(TimeSeriesEP, api_root + '/timeseries')
