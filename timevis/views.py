from timevis import app
from flask import render_template, request
from flask.ext.restful import Api, Resource, reqparse
from timevis.models import (Experiment, Layout, Factor, Channel, Level, Plate,
                            Value, session)
from timevis.transaction import get_exps, insert_exps, update_exps
from datetime import datetime
from sqlalchemy.orm import aliased
import pandas
from scikits.bootstrap import ci
from numpy import mean


@app.route('/')
def index():
    return render_template('index.html')


class ExperimentEP(Resource):
    """Endpoint for experiment information
    This endpoint mainly deals with Experiment, Channel and Factor tables.
    """
    def get(self):
        return {'experiment': get_exps()}

    def post(self):
        """Insert new Experiment records
        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        # Insert each experiment obj to table, and get list of exps inserted
        exps = insert_exps(json['experiment'])

        # Return the updated experiment obj
        return {"experiment": exps}

    def put(self):
        """Update Experiment records
        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        # Get experimen id and data body
        exps = update_exps(json['experiment'])

        # Return the updated experiment obj
        return {"experiment": exps}


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

        # Result
        ret = {"layout": []}

        for l in session.query(Layout).filter_by(id_experiment=eid).all():
            layout_obj = {}
            layout_obj["id"] = l.id
            layout_obj["name"] = l.name
            layout_obj["factors"] = []

            for f in session.query(Factor).filter_by(id_experiment=eid).all():
                fac = {}
                fac['id'] = f.id
                fac['name'] = f.name
                fac['levels'] = {}

                for well, lvl in session.query(Level.well, Level.level).\
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
        session.add_all(layouts)
        session.commit()

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

        # Get layout id and data
        for data in json["layout"]:
            # Got layout obj and modify it
            lid = data['id']
            l = session.query(Layout).filter_by(id=lid)
            l.name = data['name']

            # Update level records
            # Only update factor provided
            for f in data['factors']:
                fid = f['id']
                flvl = f['levels']
                # levels = []
                for lvl in session.query(Level).\
                        filter(Level.id_layout == lid).\
                        filter(Level.id_factor == fid).all():
                    lvl.level = flvl[lvl.well]

        # Commit the changes
        session.commit()

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

        # Return value
        ret = {"plate": []}

        # Layout obj
        l = session.query(Layout).filter_by(id=lid).first()

        # Plate inside layout
        for p in l.plates:
            p_obj = {"id": p.id, "channels": []}

            for ch in l.experiment.channels:
                ch_obj = {"id": ch.id, "name": ch.name, "value": []}
                ch_obj['time'] = [str(t[0]) for t in session.query(Value.time).
                                  distinct().order_by(Value.time).all()]
                ch_obj['well'] = [v[0] for v in session.query(Value.well).
                                  distinct().order_by(Value.well).all()]
                # Current time point
                curr_time = None
                values = None
                for v in session.query(Value).order_by(Value.time, Value.well).\
                        all():
                    if curr_time != v.time:
                        curr_time = v.time
                        # Just finish a loop
                        if values is not None:
                            ch_obj['value'].append(values)
                        # Reset
                        values = []
                    values.append(v.value)

                # Append the last time point
                ch_obj['value'].append(values)
                p_obj['channels'].append(ch_obj)

            ret["plate"].append(p_obj)
        return ret

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

        # For commit purpose
        plates = []

        # Get layout id and data
        for data in json['plate']:
            p = Plate(id_layout=lid)
            plates.append(p)

            for ch in data['channels']:
                c = session.query(Channel).filter_by(id=ch['id']).first()

                # Parse time
                time_array = [datetime.strptime(t, "%H:%M:%S").time()
                              for t in ch['time']]
                well_array = ch['well']
                for t, val_array in zip(time_array, ch['value']):
                    for well, val in zip(well_array, val_array):
                        Value(well=well, time=t, value=val, plate=p, channel=c)

        session.add_all(plates)
        try:
            session.commit()
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

        # Newly created value
        values = []

        # Get layout id and data
        for data in json['plate']:
            # Plate id
            pid = data['id']
            p = session.query(Plate).filter_by(id=pid).first()

            session.query(Value).filter_by(id_plate=pid).delete()

            for ch in data['channels']:
                c = session.query(Channel).filter_by(id=ch['id']).first()

                # Parse time
                time_array = [datetime.strptime(t, "%H:%M:%S").time()
                              for t in ch['time']]
                well_array = ch['well']
                for t, val_array in zip(time_array, ch['value']):
                    for well, val in zip(well_array, val_array):
                        values.append(Value(well=well, time=t, value=val,
                                            plate=p, channel=c))

        session.add_all(values)
        session.commit()

        # Nothing to change
        return json


class TimeSeriesEP(Resource):
    # A list of past queries
    queries = []

    def post(self):
        """
        select values.time, values.value, levels.level
            from values
                join plates
                join channels
                join levels on plates.id_layout = levels.id_layout
                join factors on levels.id_factor = factors.id
            where channels.id = 1 and
                ((factors.id=2 and
                  levels.level in ('42', 'bb')) or
                  (factors.id=1)
                );

        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Construct returning query
        query = {}
        query['experiment'] = session.query(Experiment.name).\
            filter_by(id=json['experiment']).one()[0]
        query['channel'] = session.query(Channel.name).\
            filter_by(id=json['channel']).one()[0]
        query['factors'] = []

        q = session.query(Value.time, Value.value).\
            join(Plate).\
            join(Channel).\
            filter(Channel.id == json['channel'])

        for f in json['factors']:
            Level_a = aliased(Level)
            Factor_a = aliased(Factor)
            q = q.join(Level_a, Level_a.well == Value.well).\
                join(Factor_a, Factor_a.id == Level_a.id_factor).\
                filter(Level_a.level.in_(f['levels'])).\
                filter(Factor_a.id == f['id'])
            fname = session.query(Factor.name).filter_by(id=f['id']).one()[0]
            query['factors'].append({"name": fname, "levels": f['levels']})

        # Get data frame
        df = pandas.read_sql(q.statement, q.session.bind)

        def cc(x):
            cis = ci(x)
            return (cis[1] - cis[0])/2

        # Record query
        res = {'id': len(self.queries), 'query': query, 'result': []}
        self.queries.append(json)

        df_g = df.groupby(['time']).aggregate([mean, cc])
        for row in df_g.iterrows():
            res['result'].append({
                "value": row[1][0],
                "time": str(row[0]),
                "l": row[1][0] - row[1][1],
                "u": row[1][0] + row[1][1]})

        return res


api = Api(app)
api_root = '/api/v2'
api.add_resource(ExperimentEP, api_root + '/experiment')
api.add_resource(LayoutEP,     api_root + '/layout')
api.add_resource(PlateEP,      api_root + '/plate')
api.add_resource(TimeSeriesEP, api_root + '/timeseries')
