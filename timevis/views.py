from . import app
from flask import render_template
from flask.ext import restful

api = restful.Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class Experiment(restful.Resource):
    """
    """
    pass


class Layout(restful.Resource):
    pass


class Plate(restful.Resource):
    pass


class TimeSeries(restful.Resource):
    pass

api_root = '/api/v2'
api.add_resource(Experiment, api_root + '/experiment/<string:exp_id>')
api.add_resource(Layout,     api_root + '/layout/<string:layout_id>')
api.add_resource(Plate, 	 api_root + '/plate/<string:plate_id>')
api.add_resource(TimeSeries, api_root + '/timeseries/')
