from timevis import app
from flask import render_template, request
from flask.ext import restful
import timevis.models as m

api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class Experiment(restful.Resource):
    """Endpoint for experiment information
    """
    def get(self):
        # Result
        ret = {}

        # Create query session
        s = m.Session()

        # Get Experiment instance and fill in the result dict
        for e in s.query(m.Experiment).all():
            ret[e.id] = {
                "name": e.name,
                "user": e.user,
                "well": e.well,
                "channels": [c.name for c in e.channels],
                "factors": [{"name": f.name, "type": f.type} for f in e.factors]
            }

        return ret

    def post(self):
        # Create query session
        s = m.Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # The new experiment obj should have a exp_id of 0
        data = json['0']
        e = m.Experiment(name=data['name'], user=data['user'],
                         well=data['well'])
        s.add(e)
        s.commit()

        # After commit, the e obj will obtain an id, then we can insert channels
        channels = []
        for c in data['channels']:
            channels.append(m.Channel(name=c, id_Experiment=e.id))
        s.add_all(channels)
        s.commit()

        # Insert new factors
        factors = []
        for f in data['factors']:
            factors.append(m.Factor(name=f['name'], type=f['type'],
                           id_Experiment=e.id))

        s.add_all(channels)
        s.commit()

        return ''

    def put(self):
        # Create query session
        s = m.Session()

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        # Get experimen id and data body
        eid, data = json.popitem()
        e = s.query(m.Experiment).filter_by(id=eid).first()
        e.name = data['name']
        e.user = data['user']
        e.well = data['well']
        s.commit()

        # After commit, delete the existing channels (TODO: need improvement)
        for c in s.query(m.Channel).filter_by(id_Experiment=eid).all():
            s.delete(c)
        s.commit()

        channels = []
        for c in data['channels']:
            channels.append(m.Channel(name=c, id_Experiment=e.id))
        s.add_all(channels)
        s.commit()

        # After commit, delete the existing channels (TODO: need improvement)
        for f in s.query(m.Factor).filter_by(id_Experiment=eid).all():
            s.delete(f)
        s.commit()

        # Insert new factors
        factors = []
        for f in data['factors']:
            factors.append(m.Factor(name=f['name'], type=f['type'],
                           id_Experiment=e.id))

        s.add_all(factors)
        s.commit()

        return ''


class Layout(restful.Resource):
    pass


class Plate(restful.Resource):
    pass


class TimeSeries(restful.Resource):
    pass

api_root = '/api/v2'
api.add_resource(Experiment, api_root + '/experiment')
api.add_resource(Layout,     api_root + '/layout/')
api.add_resource(Plate,      api_root + '/plate/')
api.add_resource(TimeSeries, api_root + '/timeseries/')
