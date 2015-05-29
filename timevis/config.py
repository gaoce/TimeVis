import os.path
DB_DIR = os.path.join(os.path.dirname(__file__), 'db', 'timevis.db')
DB_URL = 'sqlite:///{}'.format(DB_DIR)
