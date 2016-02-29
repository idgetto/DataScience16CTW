import os
import sys
from congress_db import DB_URL
from congress_db import create_session
from congress_db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Candidate(Base):
	__tablename__ = 'candidate'
	id = Column(String(9), nullable=False, primary_key=True)
	name = Column(String(200), nullable=True)
	party = Column(String(3), nullable=True)
	election_year = Column(String(3), nullable=True)
	office_st = Column(String(5), nullable=True)
	office = Column(String(1), nullable=True)
	office_district = Column(String(2), nullable=True)
	ici = Column(String(1), nullable=True)
	status = Column(String(1), nullable=True)
	pcc = Column(String(9), nullable=True)
	mail_street1 = Column(String(34), nullable=True)
	mail_street2 = Column(String(34), nullable=True)
	mail_city = Column(String(30), nullable=True)
	mail_state = Column(String(2), nullable=True)
	mail_zip = Column(String(9), nullable=True)

class Committee(Base):
	__tablename__ = 'committee'
	id = Column(String(9), nullable=False, primary_key=True)
	name = Column(String(200))
	treasurer = Column(String(90))
	street1 = Column(String(34))
	street2 = Column(String(34))
	city = Column(String(30))
	state = Column(String(2))
	zip = Column(String(9))
	designation = Column(String(1))
	committee_type = Column(String(1))
	party = Column(String(3))
	filling_freq = Column(String(1))
	organization_type = Column(String(1))
	organization_name = Column(String(200))
	candidate_id = Column(String(9), ForeignKey('candidate.id'))
	candidate = relationship(Candidate)

class Contribution(Base):
	__tablename__ = 'contribution'
	id = Column(Integer, nullable=False, primary_key=True)
	committee_id = Column(String(9), ForeignKey('committee.id'))
	amendment = Column(String(1))
	report_type = Column(String(3))
	tx_pgi = Column(String(5))
	image = Column(String(18))
	tx_type = Column(String(3))
	entity_type = Column(String(3))
	name = Column(String(200))
	city = Column(String(30))
	state = Column(String(2))
	zip = Column(String(9))
	employer = Column(String(38))
	occupation = Column(String(38))
	tx_date = Column(Date(), nullable=True)
	tx_amount = Column(Float(precision=2))
	other_id = Column(String(9))
	candidate_id = Column(String(9), ForeignKey('candidate.id'))
	tx_id = Column(String(32))
	file = Column(Integer)
	memo_code = Column(String(1))
	memo_text = Column(String(100))
	candidate = relationship(Candidate)
	committee = relationship(Committee)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine(DB_URL)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
