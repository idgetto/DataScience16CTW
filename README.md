# DataScience16CTW
This is the base repo for the "Change the World" project for Data Science at Olin College, Spring 2016.

## Setup

Follow these steps to run our deliverable jupyter notebook:

1. install ipywidgets, sqlalchemy, pandas, matplotlib, seaborn
2. in data/congress_db.py change the variable ROOT to the absolute path to your cloned DataScience16CTW directory
3. run `jupyter notebook deliverable/deliverable.ipynb`

## Data

### SQL Database: FEC

### rollCallVotes_cleaned.csv

In order to create the initial rollCallVotes.csv file:

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

Now in order to create the cleaned rollCallVotes.csv file, having created the initial file rollCallVotes_iter4.csv:

run 'jupyter notebook data/rollCallVotes_cleanCsv.ipynb'

The resulting rollCallVotes_clean.csv file contains the same 106 columns as rollCallVotes_iter4.csv. However it contains an additional 662 columns where each column is a topic that a piece of legislation concerned during this session of Congress. Each column contains a boolean series of 1s and 0s to determine whether or not a given bill concerns this subject.

Upon loading rollCallVotes_cleaned.csv, the code below will get all votes concerning 'Qatar' and store them in 'qatar_df': 

```python
import pandas as pd
df = pd.read_csv('../data/rollCallVotes_cleaned.csv')
qatar_df = df[df['Qatar'] == 1] 
```