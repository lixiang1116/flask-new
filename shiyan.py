from flask.ext.sqlalchemy import SQLAlchemy
import os
from untitled import db,Role

cur=Role.query.all()
for i in cur:

    print i.id,i.title,i.text

