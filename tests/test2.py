import os
import os.path
import json

# The folder holding the test data
data_path = os.path.dirname('.')

# Set the temporal config for testing
os.environ['TIMEVIS_CONFIG'] = os.path.join(data_path, 'config.py')
import timevis


app = timevis.app.test_client()
url = '/api/v2/experiment'

resp = app.get(url)
