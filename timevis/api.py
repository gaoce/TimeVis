"""Module to control the web app (restful) API

To understand how the API interacts with models (database), see also controller
module.
"""
from flask import request
from flask.ext.restful import Api, Resource, reqparse

from . import app
from . import controller as ctrl


__api_version__ = 2


class ExperimentEP(Resource):
    """Endpoint for experiment information
    """
    def get(self):
        """Return a list of Experiment objs
        """
        # Get experiment objs
        exps = ctrl.get_exps()

        return {'experiment': exps}

    def post(self):
        """Insert new Experiment records
        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        # Insert each experiment obj to table, and get list of exps inserted
        try:
            exps = ctrl.post_exps(json['experiment'])
        except Exception as e:
            return {"Error": e.message}, 500

        # Return the updated experiment obj
        return {"experiment": exps}

    def put(self):
        """Update Experiment records
        """
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        # Get experimen id and data body
        try:
            exps = ctrl.put_exps(json['experiment'])
        except Exception as e:
            return {"Error": e.message}, 500

        # Return the updated experiment obj
        return {"experiment": exps}


class LayoutEP(Resource):
    """Endpoint for layout information: namely the content of each well in a
    microplate

    This endpoint mainly query Layout, Factor and Level tables, and modify Level
    and Layout tables
    """
    def get(self):
        # Parse the request to get experiment id
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

        try:
            layouts = ctrl.post_layouts(json['layout'], eid)
        except Exception as e:
            return {"Error": e.message}, 500

        # Return newly create obj
        return {'layout': layouts}

    def put(self):
        """Update a layout's name and its levels"""
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        # TODO check input validity
        json = request.get_json(force=True)

        parser = reqparse.RequestParser()
        parser.add_argument('eid', type=int, help="experiment id")
        args = parser.parse_args()
        eid = args.eid

        try:
            layouts = ctrl.put_layouts(json['layout'], eid)
        except Exception as e:
            return {"Error": e.message}, 500

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
        """Input new plates
        """
        # Parse args
        parser = reqparse.RequestParser()
        parser.add_argument('lid', type=int, help="layout id")
        args = parser.parse_args()
        lid = args.lid

        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        try:
            plates = ctrl.post_plates(json['plate'], lid)
        except Exception as e:
            return {"Error": e.message}, 500

        return {'plate': plates}

    def put(self):
        """Update plates data"""
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        try:
            plates = ctrl.put_plates(json['plate'])
        except Exception as e:
            return {"Error": e.message}, 500

        # Nothing to change
        return {'plate': plates}


class TimeSeriesEP(Resource):
    """Endpoint for TimeSeries
    """
    # A list of past queries
    def post(self):
        # Get json from POST data, force is True so the request header don't
        # need to include "Content-type: application/json"
        json = request.get_json(force=True)

        res = ctrl.post_time(json)

        return res


api = Api(app)
api_root = '/api/v2'
api.add_resource(ExperimentEP, api_root + '/experiment')
api.add_resource(LayoutEP,     api_root + '/layout')
api.add_resource(PlateEP,      api_root + '/plate')
api.add_resource(TimeSeriesEP, api_root + '/timeseries')
