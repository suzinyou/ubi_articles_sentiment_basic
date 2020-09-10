import os
import re
import pickle

from pprint import pprint
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.sklearn

pyLDAvis.enable_notebook(local=True)

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF

from src.env import PROJECT_DIR


with open(PROJECT_DIR / 'data' / 'processed' / 'all_articles_1-morphs.pkl', 'rb') as fp:
    dfs = pickle.load(fp)

split_date = pd.Timestamp(2020, 2, 25)

all_docs_tokenized_before = []
all_docs_tokenized_after = []

for k, v in dfs.items():
    all_docs_tokenized_before.extend(v.morphs[v.index < split_date].tolist())
    all_docs_tokenized_after.extend(v.morphs[v.index >= split_date].tolist())

all_docs_tokenized = all_docs_tokenized_before + all_docs_tokenized_after

max_features = 2000
max_df = 0.4
min_df = 5

save_path = PROJECT_DIR / "models" / f"tfidf-max_features-{max_features}-max_df-{max_df}-min_df-{min_df}.pkl"
# if os.path.exists(save_path):
#     with open(save_path, "rb") as fp:
#         tfidf_vectorizer = pickle.load(fp)
#     dtm_tfidf = tfidf_vectorizer.transform([' '.join(x) for x in all_docs_tokenized])
# else:
tfidf_vectorizer = TfidfVectorizer(max_df=max_df, min_df=min_df, max_features=max_features)

dtm_tfidf = tfidf_vectorizer.fit_transform([' '.join(x) for x in all_docs_tokenized])

with open(save_path, "wb") as fp:
    pickle.dump(tfidf_vectorizer, fp)


dtm_tfidf_before = tfidf_vectorizer.transform([' '.join(x) for x in all_docs_tokenized_before])
dtm_tfidf_after = tfidf_vectorizer.transform([' '.join(x) for x in all_docs_tokenized_after])

nmf_tfidf = NMF(n_components=10, random_state=0)
nmf_tfidf.fit(dtm_tfidf)
pyLDAvis.sklearn.prepare(nmf_tfidf, dtm_tfidf, tfidf_vectorizer, mds='mmds')