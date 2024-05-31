import os
import pathlib
import pandas as pd
import sqlalchemy as sa

from models import Result, Fold, TopK
from sql import insert



def create_dataset(infos: dict, patch:int, path:pathlib.Path, region: str = None,version: int = 1):
    if region:
        return Result(name=infos['name'],
                       color=infos['color'],
                       size=infos['size'],
                       minimum=infos['minimum'],
                       features=infos['features'],
                       n_features=infos['n_features'],
                       patch=patch,
                       path=path,
                       region=region,
                       version=version)
    return Result(name=infos['name'],
                   color=infos['color'],
                   size=infos['size'],
                   minimum=infos['minimum'],
                   features=infos['features'],
                   patch=patch,
                   path=path,
                   n_features=infos['n_features'],
                   version=version)


def get_dataset_name(info: list) -> str:
    pos = next(i for i, string in enumerate(info) if 'dt=' in string)
    if pos > 0:
        return info[pos].split('=')[1]


def get_minimum(info: list) -> str:
    pos = next(i for i, string in enumerate(info) if 'm=' in string)
    if pos > 0:
        return info[pos].split('=')[1]


def get_image_size(info: list) -> str:
    pos = next(i for i, string in enumerate(info) if 'len=' in string)
    if pos > 0:
        return info[pos].split('=')[1]


def get_features(info: list) -> str:
    pos = next(i for i, string in enumerate(info) if 'ft=' in string)
    if pos > 0:
        return info[pos].split('=')[1]


def get_color(info: list) -> str:
    pos = next(i for i, string in enumerate(info) if 'c=' in string)
    if pos > 0:
        return info[pos].split('=')[1]


def get_cnn(info: list) -> str:
    pos = next(i for i, string in enumerate(info) if 'ex=' in string)
    if pos > 0:
        return info[pos].split('=')[1]

def parse_dir_name(dir_name: str) -> dict:
    if len(dir_name.split('+')) > 0:
        return {
            'name': get_dataset_name(dir_name.split('+')),
            'color': get_color(dir_name.split('+')),
            'minimum': get_minimum(dir_name.split('+')),
            'size': get_image_size(dir_name.split('+')),
            'features': get_cnn(dir_name.split('+')),
            'n_features': get_features(dir_name.split('+')),
            'region': None
        }


def exists_dataset(infos, session):
    clause = sa.and_(Result.name.__eq__(infos['name']),
                     Result.color.__eq__(infos['color']),
                     Result.minimum.__eq__(infos['minimum']),
                     Result.size.__eq__(infos['size']),
                     Result.features.__eq__(infos['features']),
                     Result.n_features.__eq__(infos['n_features']))
    return session.query(Result).filter(clause).first()

def insert_result(path: pathlib.Path, session, folds: int = 5):
    for p in pathlib.Path(path).rglob('*clf*'):
        infos = parse_dir_name(p.name)
        dataset = exists_dataset(infos, session)
        if not dataset:
            filename = os.path.join(p, 'info.csv')
            df = pd.read_csv(filename, sep=';', index_col=0, header=None, encoding='utf-8', engine='c', low_memory=False)

            dataset = create_dataset(infos, df.loc['patch', 1], str(p.resolve()), version=1)
            insert(dataset, session)

    results = session.query(Result).all()
    for result in results:
        if len(os.listdir(result.path)) > 0:
            insert_fold(folds, result, session)



def insert_fold(folds, result, session):
    for fold in range(1, folds):
        for rule in ['max', 'mult', 'sum']:
            filename = os.path.join(result.path, str(fold), 'fold+%s.csv' % rule)
            print(filename)
            df = pd.read_csv(filename, sep=';', index_col=0, header=None, engine='c', low_memory=False)
            f = Fold(fold=fold,
                     rule=rule,
                     timestamp=df.loc['time', 1],
                     f1=df.loc['f1',1],
                     accuracy=df.loc['acccuracy',1],
                     total_samples_train=df.loc['total_train_no_patch', 1],
                     total_samples_test=df.loc['total_test_no_patch', 1],
                     result_id=result.id)

            insert(f, session)
            insert_topk(f, fold, result.path, rule, session)


def insert_topk(f, fold, path, rule, session):
    filename = os.path.join(path, str(fold), 'topk', 'topk+%s.csv' % rule)
    df = pd.read_csv(filename, sep=';', index_col=False, header=0, low_memory=False, engine='c', encoding='utf8')
    for _, row in df.iterrows():
        topk = TopK(k=row['k'], scores=row['top'], scores_percent=row['percent'], rule=rule, fold_id=f.id)
        insert(topk, session)


