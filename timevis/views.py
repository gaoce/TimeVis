from . import app
from flask import render_template
from flask.ext import restful

api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class Experiment(restful.Resource):
    pass


class Layout(restful.Resource):
    pass


class Plate(restful.Resource):
    pass


class TimeSeries(restful.Resource):
    pass

api.add_resource(Experiment, '/api/v2/experiment/<string:exp_id>')
api.add_resource(Layout, '/api/v2/layout/<string:layout_id>')
api.add_resource(Plate, '/api/v2/plate/<string:plate_id>')
api.add_resource(TimeSeries, '/api/v2/timeseries/')
