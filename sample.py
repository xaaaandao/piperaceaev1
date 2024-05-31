import os
import pandas as pd
import sqlalchemy as sa

from models import  Sample
from sql import insert


def create_sample(dataset:str, minimum:int, row, region:str=None):
    return Sample(seq=row['seq'],
                  genus=row['genus'],
                  specific_epithet=row['specific_epithet'],
                  genus_trusted=row['genus_trusted'],
                  specific_epithet_trusted=row['specific_epithet_trusted'],
                  country=row['country'],
                  country_trusted=row['country_trusted'],
                  county=row['county'],
                  state_province=row['state_province'],
                  dataset=dataset,
                  minimum=int(minimum),
                  region=region)

def insert_sample(path, session):
    if session.query(Sample).count() > 0:
        return

    for dataset in ['br_dataset', 'pr_dataset']:
        for minimum in ['5', '10', '20']:
            filename = os.path.join(path, dataset, minimum, 'info_samples.csv')
            df = pd.read_csv(filename, index_col=False, header=0, sep=';', low_memory=False)
            for _, row in df.iterrows():
                sample = create_sample(dataset, minimum, row)
                insert(sample, session)
#
#
    for region in ['North', 'Northeast', 'Middlewest', 'South', 'Southeast']:
        for minimum in ['5', '10', '20']:
            filename = os.path.join(path, 'regions_dataset', region, minimum, 'info_samples.csv')
            df = pd.read_csv(filename, index_col=False, header=0, sep=';', low_memory=False)
            for _, row in df.iterrows():
                sample = create_sample('regions_dataset', minimum, row, region=region)
                insert(sample, session)