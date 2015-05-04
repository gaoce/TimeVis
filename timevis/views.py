from timevis import app
from flask import render_template
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
