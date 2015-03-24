from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from sqlalchemy.orm import Session

from singleton import singleton

@singleton
class FinanceDB:
    
    
    def __init__(self, engine_str = 'postgresql://localhost/finance'):
        self.engine_str = engine_str
        self.engine = sqlalchemy.create_engine(self.engine_str)
        self.session = Session(engine)

        self.Base = automap_base()
        self.Base.prepare(engine, reflect=True)

        self.Instrument = self.Base.classes.instrument
        self.Rongzi = self.Base.classes.rongzi
        self.Rongzi_mingxi = self.Base.classes.rongzi_mingxi

        self.query = self.session.query
        self.add = self.session.add
        self.commit = self.session.commit

    def __del__(self):
        self.session.close()
