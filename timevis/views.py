from timevis import app
from flask import render_template, request
from flask.ext.restful import Api, Resource, reqparse
from timevis.models import Experiment, Layout, Factor, Channel, Level, Session
from collections import defaultdict


@app.route('/')
def index():
    return render_template('index.html')


class ExperimentEP(Resource):
    """Endpoint for experiment information
    This endpoint mainly deals with Experiment, Channel and Factor tables.
    """
    def get(self):
        # Result
        ret = {}

        # Create query session
        s = Session()

        # Get Experiment instance and fill in the result dict
        for e in s.query(Experiment).all():
            ret[e.id] = {
                "name": e.name,
                "user": e.user,
                "well": e.well,
                "channels": [{"id": c.id, "name": c.name} for c in e.channels],
                "factors": [{"id": f.id, "name": f.name, "type": f.type}
                            for f in e.factors]
            }

        return ret

    def post(self):
        # Create query session
        s = Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # The new experiment obj should have a exp_id of 0
        data = json['0']
        e = Experiment(name=data['name'], user=data['user'], well=data['well'])
        s.add(e)
        s.commit()

        # After commit, the e obj will obtain an id, then we can insert channels
        # At this phase, the channel id from user should be 0
        channels = []
        for c in data['channels']:
            channels.append(Channel(name=c['name'], id_Experiment=e.id))
        s.add_all(channels)
        s.commit()

        # Insert new factors
        factors = []
        for f in data['factors']:
            factors.append(Factor(name=f['name'], type=f['type'],
                           id_Experiment=e.id))

        s.add_all(factors)
        s.commit()

        return 'Success'

    def put(self):
        # Create query session
        s = Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Get experimen id and data body
        eid, data = json.popitem()
        e = s.query(Experiment).filter_by(id=eid).first()
        e.name = data['name']
        e.user = data['user']
        e.well = data['well']
        s.commit()

        # After commit, delete the existing channels (TODO: need improvement)
        for c in s.query(Channel).filter_by(id_Experiment=eid).all():
            s.delete(c)
        s.commit()

        channels = []
        for c in data['channels']:
            channels.append(Channel(name=c['name'], id_Experiment=eid))
        s.add_all(channels)
        s.commit()

        # After commit, delete the existing channels (TODO: need improvement)
        for f in s.query(Factor).filter_by(id_Experiment=eid).all():
            s.delete(f)
        s.commit()

        # Insert new factors
        factors = []
        for f in data['factors']:
            factors.append(Factor(name=f['name'], type=f['type'],
                           id_Experiment=eid))

        s.add_all(factors)
        s.commit()

        return 'Success'


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
        ret = defaultdict(dict)
        # Create query session
        s = Session()

        for l in s.query(Layout).filter_by(id_Experiment=eid).all():
            ret[str(l.id)]["name"] = l.name
            ret[str(l.id)]["factors"] = []

            for f in s.query(Factor).filter_by(id_Experiment=eid).all():
                fac = {}
                fac['id'] = f.id
                fac['name'] = f.name

                for well, lvl in s.query(Level.well, Level.level).\
                        filter(Level.id_Factor == Factor.id).\
                        filter(Level.id_Layout == l.id).all():
                    fac["levels"][well] = lvl
                ret[str(l.id)]["factors"].append(fac)

        return ret

    def post(self):
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
        _, data = json.popitem()

        l = Layout(name=data['name'], id_Experiment=eid)
        s.add(l)
        s.commit()

        # After commit, the e obj will obtain an id, then we can insert channels
        lid = l.id
        levels = []
        for f in data['factors']:
            for well, level in f['levels'].items():
                levels.append(Level(well=well, level=level,
                                    id_Layout=lid, id_Factor=f['id']))
        s.add_all(levels)
        s.commit()

        return 'Success'

    def put(self):
        """ Update a layout's name and its levels"""

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Get layout id and data
        lid, data = json.popitem()

        # Create query session
        s = Session()

        # Got layout obj and modify it
        l = s.query(Layout).filter_by(id=lid)
        l.name = data['name']
        s.commit()

        # Update level records
        # Only update factor provided
        for f in data['factors']:
            for lvl in s.query(Level).filter(Level.id_Layout == lid).\
                    filter(Level.id_Factor == f['id']).all():
                lvl.level = f['levels'][lvl.well]
        s.commit()

        return 'Success'


class PlateEP(Resource):
    pass


class TimeSeriesEP(Resource):
    pass

api = Api(app)
api_root = '/api/v2'
api.add_resource(ExperimentEP, api_root + '/experiment')
api.add_resource(LayoutEP,     api_root + '/layout')
api.add_resource(PlateEP,      api_root + '/plate')
api.add_resource(TimeSeriesEP, api_root + '/timeseries')
