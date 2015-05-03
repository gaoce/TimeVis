from . import app
from flask import render_template
from flask.ext import restful

api = restful.Api(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/test')
def test():
    return render_template('control.html')


class Experiment(restful.Resource):
    pass


class Layout(restful.Resource):
    pass


class Plate(restful.Resource):
    pass


class TimeSeries(restful.Resource):
    pass

api.add_resource(Experiment, '/experiment')
api.add_resource(Layout, '/layout')
api.add_resource(Plate, '/plate')
api.add_resource(TimeSeries, '/timeseries/')
