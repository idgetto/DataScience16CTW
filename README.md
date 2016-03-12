# DataScience16CTW
This is the base repo for the "Change the World" project for Data Science at Olin College, Spring 2016.

## Setup

Follow these steps to run our deliverable jupyter notebook:

1. install ipywidgets, sqlalchemy, pandas, matplotlib, seaborn
2. in data/congress_db.py change the variable ROOT to the absolute path to your cloned DataScience16CTW directory
3. run `jupyter notebook deliverable/deliverable.ipynb`

## Data

### SQL Database: FEC

One source of our data for this project was from the [FEC website](http://www.fec.gov/finance/disclosure/ftpdet.shtml#a2015_2016). The FEC provides detailed information about candidates running for the senate, house, and presidency as well as contribution information related to committees.

We used three files from the FEC:

* The Candidate Master File
* The Committee Master File
* The Contributions to Candidate from Committees file

Using these three files, we setup a sqlite database with sqlalchemy as our object relational mapper. The code that creates the database can be found in [data/congress_db.py](./data/setup_db.py) and [data/seed_db.py](./data/seed_db.py). In `setup_db.py` we create three tables `Candidate`, `Committee`, and `Contribution`. We then make queries to the database to find information related to each of the tables.

The tables contain the following data:

### Candidate

| **Column**        | **Contains**                                                                                                                                                 |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`              | a 9-character alpha-numeric code assigned to a candidate by the Federal Election Commission.                                                                 |
| `name`            | candidate's name                                                                                                                                             |
| `party`           | candidate's party                                                                                                                                            |
| `election_year`   | candidate's election year                                                                                                                                    |
| `office_st`       | candidate's state of representation                                                                                                                          |
| `office`          | office that the candidate is running for (H=House, P=President, S=Senate)                                                                                    |
| `office_district` | candidate's congressional district number                                                                                                                    |
| `ici`             | incumbent challenger status (C=Challenger, I=Incumbent, O=Open Seat)                                                                                         |
| `status`          | candidate's status (C=Statutory candidate, F=Statutory candidate for future election, N=Not yet a statutory candidate, P=Statutory candidate in prior cycle) |
| `pcc`             | candidate's principal campaign committee ID                                                                                                                  |
| `mail_street1`    | candidate's mailing address street line 1                                                                                                                    |
| `mail_street2`    | candidate's mailing address street line 2                                                                                                                    |
| `mail_state`      | candidate's mailing address state

### Committee

| **Column**          | **Contains**                                                                                                                                                                        |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`                | a 9-character alpha-numeric code assigned to a committee by the Federal Election Commission                                                                                         |
| `name`              | committee's name                                                                                                                                                                    |
| `treasurer`         | officially registered treasurer for the committee                                                                                                                                   |
| `street1`           | committee street address line 1                                                                                                                                                     |
| `street2`           | committee street address line 2                                                                                                                                                     |
| `city`              | committee city                                                                                                                                                                      |
| `state`             | committee state                                                                                                                                                                     |
| `zip`               | committee zip code                                                                                                                                                                  |
| `designation`       | committee designation (A=Authorized by a candidate, B=Lobbyist/Registrant PAC, D=Leadership PAC, J=Joint fundraiser, P=Principal campaign committee of a candidate, U=Unauthorized) |
| `committee_type`    | type of committee; [committee types](http://www.fec.gov/finance/disclosure/metadata/CommitteeTypeCodes.shtml)                                                                       |
| `party`             | political party associated with committee; [party list](http://www.fec.gov/finance/disclosure/metadata/DataDictionaryPartyCodeDescriptions.shtml)                                   |
| `filling_freq`      | frequency of committee reports (A=Administratively terminated ,D=Debt, M=Monthly filer ,Q=Quarterly filer, T=Terminated, W=Waived)                                                  |
| `organization_type` | interest group category (C=Corporation, L=Labor organization, M=Membership organization, T=Trade association, V=Cooperative, W=Corporation without capital stock)                   |
| `organization_name` | connected organization's name                                                                                                                                                       |
| `candidate_id`      | id of associated candidate

### Contribution

| **Column**     | **Contains**                                                                                                                                                                                                   |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `id`           | unique contribution id                                                                                                                                                                                         |
| `committee_id` | a 9-character alpha-numeric code assigned to a committee by the Federal Election Commission                                                                                                                    |
| `amendment`    | indicates if the report being filed is new (N), an amendment (A) to a previous report, or a termination (T) report                                                                                             |
| `report_type`  | type of report; [report types](http://www.fec.gov/finance/disclosure/metadata/ReportTypeCodes.shtml)                                                                                                           |
| `tx_pgi`       | code indicates the,election for which the contribution was made                                                                                                                                                |
| `entity_type`  | type of entity (CAN=Candidate, CCM=Candidate Committee, COM=Committee, IND=Individual (a person), ORG=Organization (not a committee and not a person), PAC=Political Action Committee, PTY=Party Organization) |
| `name`         | recipient/payee                                                                                                                                                                                                |
| `city`         | city/town                                                                                                                                                                                                      |
| `state`        | state                                                                                                                                                                                                          |
| `zip`          | zip code                                                                                                                                                                                                       |
| `employer`     | employer                                                                                                                                                                                                       |
| `occupation`   | occupation                                                                                                                                                                                                     |
| `tx_date`      | transaction date                                                                                                                                                                                               |
| `tx_amount`    | transaction amount                                                                                                                                                                                             |
| `other_id`     | FEC ID of the recipient committee or the supported or opposed candidate ID                                                                                                                                     |
| `candidate_id` | id if candidate receiving the contribution                                                                                                                                                                     |
| `tx_id`        | unique identifier associated with each itemization or transaction appearing in an FEC electronic file                                                                                                          |
| `file`         | unique report id                                                                                                                                                                                               |
| `memo_code`    | memo code                                                                                                                                                                                                      |
| `memo_text`    | description of the activity                                                                                                                                                                                    |

### Querying Contribution Data

We use sqlalchemy in order to query data from the contribution database. For example, we can find the total contribution amount of candidates grouped by state.

```python
import congress_db
from setup_db import Candidate, Contribution, Committee
from sqlalchemy import func

session = congress_db.create_session()

session.query(Candidate.office_st,
              func.sum(Contribution.tx_amount).label('total_contr')).\
        join(Contribution).\
        group_by(Candidate.office_st).\
        order_by('total_contr desc').\
        all()

# => [(u'US', 110900511.0), (u'CA', 94463385.0), (u'NC', 86051685.0), ...]
```

### rollCallVotes_cleaned.csv

In order to create the initial rollCallVotes_iter4.csv file:

1. install bs4, lxml, pandas
2. run 'jupyter notebook data/rollCallVotes_createCsv.ipynb'

In the resulting rollCallVotes_iter4.csv file, each row is a roll call vote that occurred in the US Senate during the first session of the 114th Congress. The first 100 columns contain each senator as a string in the following format:

`Last_name (Party-State)`

There are 6 columns remaining and are organized as such:

Column | Contains
--- | ---
`billTitle` | the title used by congress.gov to refer to this legislation
`sponsor` | the senator who sponsored this legislation
`subjects` | a list, stored as a string, of all subjects this legislation concerns according to congress.gov
`title`	| since amendments on congress.gov do not contain subjects, links amendments to each bill to find the corresponding subjects
`voteDate` | the date of the roll call vote
`voteResult` | the result of the vote

Now in order to create the rollCallVotes_cleaned.csv file, having created the initial file rollCallVotes_iter4.csv:

run 'jupyter notebook data/rollCallVotes_cleanCsv.ipynb'

The resulting rollCallVotes_clean.csv file contains the same 106 columns as rollCallVotes_iter4.csv. However it contains an additional 662 columns where each column is a topic that a piece of legislation concerned during this session of Congress. Each column contains a boolean series of 1s and 0s to determine whether or not a given bill concerns this subject.

Upon loading rollCallVotes_cleaned.csv, the code below will get all votes concerning 'Qatar' and store them in 'qatar_df':

```python
import pandas as pd
df = pd.read_csv('../data/rollCallVotes_cleaned.csv')
qatar_df = df[df['Qatar'] == 1]
```
