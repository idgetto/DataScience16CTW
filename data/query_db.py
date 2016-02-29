import congress_db
from setup_db import Candidate, Contribution, Committee

session = congress_db.create_session()
print session.query(Committee).count()
print session.query(Committee).first()
