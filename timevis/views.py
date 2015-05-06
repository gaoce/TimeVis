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
        ret = {"experiment": []}

        # Create query session
        s = Session()

        # Get Experiment instance and fill in the result dict
        for e in s.query(Experiment).all():
            ret["experiment"].append({
                "name": e.name,
                "user": e.user,
                "well": e.well,
                "channels": [{"id": c.id, "name": c.name} for c in e.channels],
                "factors": [{"id": f.id, "name": f.name, "type": f.type}
                            for f in e.factors]})

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

        # The new experiment obj should have a exp_id of 0
        for data in json['experiment']:
            e = Experiment(name=data['name'], user=data['user'],
                           well=data['well'])
            s.add(e)
            s.commit()

            # After commit, the exp will have an id, we can insert channels now.
            channels = []
            for c in data['channels']:
                channels.append(Channel(name=c['name'], id_Experiment=e.id))
            s.add_all(channels)

            # Insert new factors
            factors = []
            for f in data['factors']:
                factors.append(Factor(name=f['name'], type=f['type'],
                               id_Experiment=e.id))

            s.add_all(factors)

            # Commit the changes for channels and factors
            s.commit()

        return 'Success'

    def put(self):
        """Update experiment information:
            1. Update experiment record;
            2. Delete channel and factor records associated
            3. Add new channel and factor records
        """
        # Create query session
        s = Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Get experimen id and data body
        for data in json['experiment']:
            eid = data['id']
            e = s.query(Experiment).filter_by(id=eid).first()
            e.name = data['name']
            e.user = data['user']
            e.well = data['well']

            # Delete associated channel and factor records
            for c, f in s.query(Channel, Factor).\
                    filter(Channel.id_Experiment == eid).\
                    filter(Factor.id_Experiment == eid).\
                    all():
                s.delete(c)
                s.delete(f)

            # Insert new channels
            channels = []
            for c in data['channels']:
                channels.append(Channel(name=c['name'], id_Experiment=eid))
            s.add_all(channels)

            # Insert new factors
            factors = []
            for f in data['factors']:
                factors.append(Factor(name=f['name'], type=f['type'],
                               id_Experiment=eid))

            s.add_all(factors)

            # Commit the changes
            # TODO try except
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

        # TODO return meaningful result
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
