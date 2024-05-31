import os

import pandas as pd

from models import TopK
from sql import insert


def insert_topk(fold, path, rule, session):
    filename = os.path.join(path, str(fold), 'topk', 'topk+%s.csv' % rule)
    df = pd.read_csv(filename, sep=';', index_col=False, header=0, low_memory=False, engine='c', encoding='utf8')
    for _, row in df.iterrows():
        topk = TopK(k=row['k'], scores=row['top'], scores_percent=row['percent'], fold=fold.id)
        insert(topk, session)
