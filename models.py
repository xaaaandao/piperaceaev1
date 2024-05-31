from typing import Optional, List

import sqlalchemy as sa
import sqlalchemy.ext.declarative
from sqlalchemy.orm import Mapped

Base = sa.ext.declarative.declarative_base()


def get_base():
    return Base



class Result(Base):
    __tablename__ = 'result'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    region = sa.Column(sa.String, nullable=True)
    color = sa.Column(sa.String, nullable=True)
    size = sa.Column(sa.Integer, nullable=True)
    minimum = sa.Column(sa.Integer, nullable=True)
    version = sa.Column(sa.Integer, nullable=True)
    features = sa.Column(sa.String, nullable=True)
    n_features = sa.Column(sa.Integer, nullable=True)
    patch = sa.Column(sa.Integer, nullable=True)
    path = sa.Column(sa.String, nullable=True)
    # samples: Mapped[List['Sample']] = sa.orm.relationship(
    #     secondary='dataset_sample', back_populates='datasets'
    # )
    #
    # sample_associations: Mapped[List['DatasetSample']] = sa.orm.relationship(
    #     back_populates='dataset'
    # )
    fold: sa.orm.Mapped['Fold'] = sa.orm.relationship(back_populates='result')



class Fold(Base):
    __tablename__ = 'fold'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    fold = sa.Column(sa.Integer, nullable=True)
    rule = sa.Column(sa.String, nullable=True)
    timestamp = sa.Column(sa.String, nullable=True)
    f1: float = sa.Column(sa.Float, nullable=True)
    accuracy: float = sa.Column(sa.Float, nullable=True)
    total_samples_train: int = sa.Column(sa.Integer, nullable=True)
    total_samples_test: int = sa.Column(sa.Integer, nullable=True)
    result_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('result.id'))
    result: sa.orm.Mapped['Result'] = sa.orm.relationship(back_populates='fold')
    topk: sa.orm.Mapped['TopK'] = sa.orm.relationship(back_populates='fold')


class TopK(Base):
    __tablename__ = 'topk'

    id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    k = sa.Column(sa.Integer, nullable=True)
    scores = sa.Column(sa.Float, nullable=True)
    scores_percent = sa.Column(sa.Float, nullable=True)
    rule = sa.Column(sa.String, nullable=True)
    fold_id: sa.orm.Mapped[int] = sa.orm.mapped_column(sa.ForeignKey('fold.id'))
    fold: sa.orm.Mapped['Fold'] = sa.orm.relationship(back_populates='topk')

# class Mean(Base):
#     id: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
#     fold: sa.Column(sa.Integer, nullable=True)
#     rule: sa.Column(sa.String, nullable=True)
#     f1: float = sa.Column(sa.Float, nullable=True)
#     std_f1: float = sa.Column(sa.Float, nullable=True)
#     accuracy: float = sa.Column(sa.Float, nullable=True)
#     std_accuracy: float = sa.Column(sa.Float, nullable=True)

class Sample(Base):
    __tablename__ = 'samples'

    seq: sa.orm.Mapped[int] = sa.orm.mapped_column(primary_key=True, autoincrement=True)
    genus = sa.Column(sa.String, nullable=True)
    specific_epithet = sa.Column(sa.String, nullable=True)
    genus_trusted = sa.Column(sa.String, nullable=True)
    specific_epithet_trusted = sa.Column(sa.String, nullable=True)
    country = sa.Column(sa.String, nullable=True)
    country_trusted = sa.Column(sa.String, nullable=True)
    county = sa.Column(sa.String, nullable=True)
    state_province = sa.Column(sa.String, nullable=True)
    dataset = sa.Column(sa.String, nullable=True)
    region = sa.Column(sa.String, nullable=True)
    minimum = sa.Column(sa.Integer, nullable=True)

