import os.path
DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'timevis.db')
DB_URL = 'sqlite:///{}'.format(DB_PATH)
