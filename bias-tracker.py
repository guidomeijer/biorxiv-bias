# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 11:55:34 2021

@author: guido
"""

import numpy as np
import pandas as pd
import gender_guesser.detector as gender
from biorxiv_retriever import BiorxivRetriever
br = BiorxivRetriever(search_engine='rxivist')
d = gender.Detector()

# Settings
TOP = 10  # how many top papers to query
METRIC = 'twitter'  # twitter or downloads
TIME = 'week'  # day or week

# Query top papers of today
papers = br.query(f'&timeframe={TIME}&metric={METRIC}', full_text=False, metadata=False)

# Get all author genders
authors = pd.DataFrame()
for i, paper in enumerate(papers):
    for j, author in enumerate(paper['authors']):
        authors = authors.append(pd.DataFrame(index=[authors.shape[0]+1], data={
            'name': author['name'],
            'gender': d.get_gender(author['name'].split()[0]),
            'position': i + 1}))

# Calculate percentage female
authors_select = authors[(authors['gender'] != 'unknown') & (authors['gender'] != 'andy')]
perc_all = (np.sum(authors_select['gender'].str.contains('female'))
            / authors_select.shape[0]) * 100
perc_top = (np.sum(authors_select[authors_select['position'] <= TOP]['gender'].str.contains('female'))
            / authors_select[authors_select['position'] <= TOP].shape[0]) * 100
print(f'{perc_all:.1f}% female in all papers')
print(f'{perc_top:.1f}% female in top {TOP} most tweeted papers')




