#!/usr/bin/env python
import timevis
import timevis.models as m


def init_db():
    m.Base.metadata.create_all(m.engine)

init_db()
timevis.app.run(host='0.0.0.0', port=8000)
