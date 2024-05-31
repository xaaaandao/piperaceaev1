import os

import pandas as pd

from database import connect, close
from result import insert_result
from sample import insert_sample
from sql import insert
from models import TopK, get_base


def insert_topk(fold, path, session):
    for rule in ['max', 'mult', 'sum']:
        filename = os.path.join(path, str(fold), 'topk', 'topk+%s.csv' % rule)
        df = pd.read_csv(filename, sep=';', index_col=False, header=0, low_memory=False, engine='c', encoding='utf8')
        for _, row in df.iterrows():
            topk = TopK(k=row['k'], scores=row['top'], scores_percent=row['percent'], fold=fold.id)
            insert(topk, session)



def main():
    engine, session = connect(database='herbariov1')

    base = get_base()
    # if not sa.inspect(engine).has_table(Dataset.__tablename__):
    #     base.metadata.tables[Dataset.__tablename__].create(bind=engine)

    base.metadata.create_all(engine)

    insert_sample('./datasets', session)
    insert_result('./results', session)

    close(engine, session)


if __name__ == '__main__':
    main()
