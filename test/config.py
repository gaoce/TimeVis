import tempfile

_, DB_PATH = tempfile.mkstemp()
DB_URL = 'sqlite:///{}'.format(DB_PATH)
