from timevis import app
from flask import render_template, request
from flask.ext.restful import Api, Resource, reqparse
from timevis.models import Experiment, Layout, Factor, Channel, Level, Session


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

        # Return the updated experiment obj
        e_new = s.query(Experiment).filter_by(id=e.id).first()
        return {"experiment": [self.construct_exp(e_new)]}

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
            if e is None:
                return ''
            e.name = data['name']
            e.user = data['user']
            e.well = data['well']

            # TODO update without delete
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

            # TODO: UPDATE level table factor id

            # Commit the changes
            # TODO try except
            s.commit()

        # Return the updated experiment obj
        e = s.query(Experiment).filter_by(id=eid).first()
        return {"experiment": [self.construct_exp(e)]}

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

        for l in s.query(Layout).filter_by(id_Experiment=eid).all():
            layout_obj = {}
            layout_obj["id"] = l.id
            layout_obj["name"] = l.name
            layout_obj["factors"] = []

            for f in s.query(Factor).filter_by(id_Experiment=eid).all():
                fac = {}
                fac['id'] = f.id
                fac['name'] = f.name
                fac['levels'] = {}

                for well, lvl in s.query(Level.well, Level.level).\
                        filter(Level.id_Factor == f.id).\
                        filter(Level.id_Layout == l.id).all():
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
        for idx, data in enumerate(json["layout"]):

            # Create a new Layout record
            l = Layout(name=data['name'], id_Experiment=eid)
            s.add(l)
            s.commit()

            # Update level records
            levels = []
            lid = data['id'] = l.id
            for f in data['factors']:
                fid = f['id']
                for well, level in f['levels'].items():
                    levels.append(Level(well=well, level=level,
                                        id_Layout=lid, id_Factor=fid))

            s.add_all(levels)
            s.commit()

            # Only Layout id is changed (a new one is given)
            json['layout'][idx]['id'] = lid

        # Return newly create obj
        return json

    def put(self):
        """ Update a layout's name and its levels"""
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
                        filter(Level.id_Layout == lid).\
                        filter(Level.id_Factor == fid).all():
                    lvl.level = flvl[lvl.well]

        # Commit the changes
        s.commit()

        # Nothing to change, really
        return json


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
