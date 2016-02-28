from congress_db import create_session
from setup_db import Candidate, Committee, Contribution
import datetime

def seed():
	seed_candidates()
	seed_contributions()
	seed_committees()

def seed_candidates():
	import pandas as pd
	from setup_db import Candidate

	session = create_session()
	candidates = pd.read_csv('candidates.tsv', sep='\t')

	# Check if seeding has already been done
	num_candidates= len(candidates)
	num_candidates_imported = session.query(Candidate).count()
	if num_candidates_imported == num_candidates:
		return

	print 'Importing candidates...'
	for (idx, cand_data) in candidates.iterrows():

		if idx % 1000 == 0:
			print 'Imported %d candidates' % idx

		candidate = Candidate(id 			  = cand_data.CAND_ID,
							  name 			  = cand_data.CAND_NAME,
							  party 		  = cand_data.CAND_PTY_AFFILIATION,
							  election_year   = cand_data.CAND_ELECTION_YR,
							  office_st 	  = cand_data.CAND_OFFICE_ST,
							  office 	      = cand_data.CAND_OFFICE,
							  office_district = cand_data.CAND_OFFICE_DISTRICT,
							  ici 			  = cand_data.CAND_ICI,
							  status 		  = cand_data.CAND_STATUS,
							  pcc 			  = cand_data.CAND_PCC,
							  mail_street1 	  = cand_data.CAND_ST1,
							  mail_street2 	  = cand_data.CAND_ST2,
							  mail_city 	  = cand_data.CAND_CITY,
							  mail_state 	  = cand_data.CAND_ST,
							  mail_zip 		  = cand_data.CAND_ZIP)

		session.add(candidate)

	# Save changes
	session.commit()

	num_candidates = len(candidates)
	num_candidates_imported = session.query(Candidate).count()
	print "%d of %d candidates imported." % (num_candidates_imported, num_candidates)

def seed_contributions():
	import pandas as pd
	from setup_db import Contribution

	session = create_session()

	col_types = {
		'SUB_ID': int,
		'CMTE_ID': str,
		'AMNDT_IND': str,
		'RPT_TP': str,
		'TRANSACTION_PGI': str,
		'IMAGE_NUM': str,
		'TRANSACTION_TP': str,
		'ENTITY_TP': str,
		'NAME': str,
		'CITY': str,
		'STATE': str,
		'ZIP_CODE': str,
		'EMPLOYER': str,
		'OCCUPATION': str,
		'TRANSACTION_DT': str,
		'TRANSACTION_AMT': float,
		'OTHER_ID': str,
		'CAND_ID': str,
		'TRAN_ID': str,
		'FILE_NUM': int,
		'MEMO_CD': str,
		'MEMO_TEXT': str
	}
	contributions = pd.read_csv('contributions.tsv', sep='\t', dtype=col_types)

	# Check if seeding has already been done
	num_contributions = len(contributions)
	num_contributions_imported = session.query(Contribution).count()
	if num_contributions_imported == num_contributions:
		return

	print 'Importing contributions...'
	for (idx, contra_data) in contributions.iterrows():
		if idx % 1000 == 0:
			print 'Imported %d contributions' % idx

		try:
			tx_date_str = contra_data.TRANSACTION_DT
			tx_date = datetime.datetime.strptime(tx_date_str, "%m%d%Y").date()
		except:
			tx_date = None

		contribution = Contribution(id 			 = contra_data.SUB_ID,
									committee_id = contra_data.CMTE_ID,
									amendment 	 = contra_data.AMNDT_IND,
									report_type  = contra_data.RPT_TP,
									tx_pgi 		 = contra_data.TRANSACTION_PGI,
									image 		 = contra_data.IMAGE_NUM,
									tx_type 	 = contra_data.TRANSACTION_TP,
									entity_type  = contra_data.ENTITY_TP,
									name 	     = contra_data.NAME,
									city 		 = contra_data.CITY,
									state 		 = contra_data.STATE,
									zip 		 = contra_data.ZIP_CODE,
									employer 	 = contra_data.EMPLOYER,
									occupation 	 = contra_data.OCCUPATION,
									tx_date 	 = tx_date,
									tx_amount 	 = contra_data.TRANSACTION_AMT,
									other_id 	 = contra_data.OTHER_ID,
									candidate_id = contra_data.CAND_ID,
									tx_id 		 = contra_data.TRAN_ID,
									file 		 = contra_data.FILE_NUM,
									memo_code 	 = contra_data.MEMO_CD,
									memo_text 	 = contra_data.MEMO_TEXT)

		session.add(contribution)

	# Save changes
	session.commit()

	num_contributions = len(contributions)
	num_contributions_imported = session.query(Contribution).count()
	print "%d of %d contributions imported." % (num_contributions_imported, num_contributions)

def seed_committees():
	import pandas as pd
	from setup_db import Committee

	session = create_session()
	committees = pd.read_csv('committees.tsv', sep='\t', dtype=str)

	# Check if data is already imported
	num_committees = len(committees)
	num_committees_imported = session.query(Committee).count()
	if (num_committees_imported == num_committees):
		return

	print 'Importing candidates...'
	for (idx, comm_data) in committees.iterrows():
		if idx % 1000 == 0:
			print 'Imported %d committees' % idx

		committee = Committee(id   			 	= comm_data.CMTE_ID,
							  name 			 	= comm_data.CMTE_NM,
							  treasurer      	= comm_data.TRES_NM,
							  street1 		 	= comm_data.CMTE_ST1,
							  street2 	     	= comm_data.CMTE_ST2,
							  city 		     	= comm_data.CMTE_CITY,
							  state 		 	= comm_data.CMTE_ST,
							  zip 			 	= comm_data.CMTE_ZIP,
							  designation 	 	= comm_data.CMTE_DSGN,
							  committee_type 	= comm_data.CMTE_TP,
							  party 		 	= comm_data.CMTE_PTY_AFFILIATION,
							  filling_freq      = comm_data.CMTE_FILING_FREQ,
							  organization_type = comm_data.ORG_TP,
							  organization_name = comm_data.CONNECTED_ORG_NM,
							  candidate_id 		= comm_data.CAND_ID)

		session.add(committee)

	# Save changes
	session.commit()

	num_committees = len(committees)
	num_committees_imported = session.query(Committee).count()
	print "%d of %d committees imported." % (num_committees_imported, num_committees)

if __name__ == '__main__':
	seed()
