from timevis import app
from flask import request
from flask.ext.restful import Api, Resource, reqparse
from timevis.models import (Experiment, Factor, Channel, Level, Plate,
                            Value, session)
import timevis.controller as ctrl
from sqlalchemy.orm import aliased
import pandas
from scikits.bootstrap import ci
from numpy import mean


class ExperimentEP(Resource):
    """Endpoint for experiment information
    This endpoint mainly deals with Experiment, Channel and Factor tables.
    """
    def get(self):
        # Experiment objs
        exps = ctrl.get_exps()

        return {'experiment': exps}

    def post(self):
        """Insert new Experiment records
        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        # Insert each experiment obj to table, and get list of exps inserted
        exps = ctrl.insert_exps(json['experiment'])

        # Return the updated experiment obj
        return {"experiment": exps}

    def put(self):
        """Update Experiment records
        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        # Get experimen id and data body
        exps = ctrl.update_exps(json['experiment'])

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

        # Layout objs
        layouts = ctrl.get_layouts(eid)

        return {"layout": layouts}

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
        json = request.get_json(force=True)

        layouts = ctrl.post_layouts(json['layout'], eid)

        # Return newly create obj
        return {'layout': layouts}

    def put(self):
        """Update a layout's name and its levels"""
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        layouts = ctrl.put_layouts(json['layout'])

        # Nothing to change, really
        return {'layout': layouts}


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
        plates = ctrl.get_plates(lid)

        return {'plate': plates}

    def post(self):
        """Input new plates"""

        # Parse args
        parser = reqparse.RequestParser()
        parser.add_argument('lid', type=int, help="layout id")
        args = parser.parse_args()
        lid = args.lid

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        plates = ctrl.post_plates(json['plate'], lid)

        return {'plate': plates}

    def put(self):
        """Update plates data"""
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        plates = ctrl.put_plates(json['plate'])

        # Nothing to change
        return {'plate': plates}


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
