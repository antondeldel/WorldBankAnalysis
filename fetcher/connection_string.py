from sqlalchemy import create_engine
import os
p = os.path.join(os.getcwd(),'data','temporary.sqlite3')
engine = create_engine('sqlite:///data/temporary.sqlite3',echo=True)
#engine = create_engine('sqlite:////'+p,echo=True)
