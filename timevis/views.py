from timevis import app
from flask import render_template, request
from flask.ext import restful
import timevis.models as m

api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class Experiment(restful.Resource):
    """
    """
    def get(self):
        # Result
        res = {}

        # Create query session
        s = m.Session()

        # Get Experiment instance and fill in the result dict
        for e in s.query(m.Experiment).all():
            res[e.id] = {
                "name": e.name,
                "users": e.user,
                "well": e.well,
                "channels": [c.name for c in e.channels],
                "factors": [{"name": f.name, "type": f.type} for f in e.factors]
            }

        return res

    def post(self):
        # Create query session
        s = m.Session()

        data = request.get_json()['0']
        e = m.Experiment(name=data['name'], user=data['user'],
                         well=data['well'])
        s.add(e)
        s.commit()

        channels = []
        for c in data['channels']:
            channels.append(m.Channel(name=c, id_Experiment=e.id))
        s.add_all(channels)
        s.commit()

        factors = []
        for f in data['factors']:
            factors.append(m.Factor(name=f['name'], type=f['type'],
                           id_Experiment=e.id))

        s.add_all(channels)
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
