import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd

import sys
sys.path.append('../data')

import congress_db
from setup_db import Candidate, Contribution, Committee
from sqlalchemy import func

import datetime
from collections import OrderedDict

session = congress_db.create_session()

from itertools import groupby
def month_grouper(data):
	item = data[0]
	return item.year, item.month

def bin_contributions_by_month(contributions):
	grouped = groupby(contributions, month_grouper)

	monthly_dollars = {}
	for ((year, month), data) in grouped:
		d = datetime.date(year, month, 1)
		for (_, dollars) in data:
			monthly_dollars[d] = monthly_dollars.get(d, 0) + dollars

	return monthly_dollars

def monthly_dollars_by_party(party, start_date=None, end_date=None):
	if not start_date:
		start_date = datetime.date(2013, 1, 1)
	if not end_date:
		end_date = datetime.date(2016, 1, 1)

	party_contributions = session.query(Contribution.tx_date, func.sum(Contribution.tx_amount)).\
									group_by(Contribution.tx_date).\
									join(Candidate).\
									filter(Candidate.party == party).\
									filter(Contribution.tx_date != None).\
									filter(Contribution.tx_date >= start_date).\
									filter(Contribution.tx_date < end_date).\
									all()

	monthly_dollars = bin_contributions_by_month(party_contributions)

	# find all months
	all_dates = map(datetime.date.fromordinal, range(start_date.toordinal(), end_date.toordinal()))
	all_months = filter(lambda d: d.day == 1, all_dates)

	for d in all_months:
		monthly_dollars[d] = monthly_dollars.get(d, 0)

	return OrderedDict(sorted(monthly_dollars.items()))

def plot_monthly_dollars_by_party(party, color='blue', start_date=None, end_date=None, election_date=None):
	monthly_dollars = monthly_dollars_by_party(party, start_date, end_date)
	months, dollars = monthly_dollars.keys(), monthly_dollars.values()

	plt.plot(range(len(months)), dollars, 'o-', color=color, label=party)

	# label every other month
	xtick_locs = range(0, len(months), 2)
	xtick_labels = [d.strftime('%B %Y') for d in months[::2]]
	plt.xticks(xtick_locs, xtick_labels, rotation=70)

	# format for dollars
	a = plt.gca()
	a.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

	# show election day
	if election_date:
		first_date = months[0]
		date_diff = election_date - first_date
		months_diff = date_diff.days / 30.0

		plt.axvline(months_diff, color='black', ls='dashed', label='Election Day')

	plt.xlim((0, len(months)-1))
	plt.ylabel('Total Monthly Contributions ($)')
	plt.title('Total Monthly Contributions')
	plt.legend(loc='upper right')
