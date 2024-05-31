import importlib
import inspect
import os

import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema

# from models import Exsiccata
# from unaccent import unaccent


def connect(echo: bool = True, host: str = 'localhost', user: str = os.environ['PGUSER'],
            password: str = os.environ['PGPWD'], port: str = '5432', database: str = 'herbario'):
    try:
        url = sa.URL.create(
            'postgresql+psycopg2',
            username=user,
            password=password,
            host=host,
            database=database,
            port=port
        )
        engine = sa.create_engine(url, echo=echo, pool_pre_ping=True)
        session = sqlalchemy.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        if engine.connect():
            return engine, session()
    except Exception as e:
        print(e)


# def update_country_trusted(session, query):
#     uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower = get_list_uf_state_county(query)
#     condition = sa.and_(Exsiccata.country_trusted.is_(None),
#                         sa.or_(uf_unaccented_lower, state_unaccented_lower))
#     try:
#         session.query(Exsiccata) \
#             .filter(condition) \
#             .update({'country_trusted': 'Brasil'}, synchronize_session=False)
#         session.commit()
#     except Exception as e:
#         print(e)
#         session.flush()
#
#
# def get_list_uf_state_county(query):
#     list_uf = [unaccent(sa.func.lower(q.uf)) for q in query]
#     list_state = [unaccent(sa.func.lower(q.state)) for q in query]
#     list_county = [unaccent(sa.func.lower(q.county)) for q in query]
#
#     uf_unaccented_lower = unaccent(sa.func.lower(Exsiccata.state_province)).in_(list_uf)
#     state_unaccented_lower = unaccent(sa.func.lower(Exsiccata.state_province)).in_(list_state)
#     county_unaccented_lower = unaccent(sa.func.lower(Exsiccata.county)).in_(list_county)
#
#     return uf_unaccented_lower, state_unaccented_lower, county_unaccented_lower
#
#
# def get_columns_table(table):
#     return table.__table__.columns
#
#
# def get_records_group_by_level(condition, level, minimum_image, session):
#     columns = [level,
#                sa.func.array_agg(Exsiccata.seq).label('list_seq')]
#     query = session.query(*columns) \
#         .filter(condition) \
#         .distinct() \
#         .group_by(level) \
#         .order_by(level) \
#         .having(sa.func.count(level) >= minimum_image) \
#         .all()
#     return query
#
#
# def get_state_uf_county(query):
#     list_uf = [unaccent(sa.func.lower(q.uf)) for q in query]
#     list_state = [unaccent(sa.func.lower(q.state)) for q in query]
#     list_county = [unaccent(sa.func.lower(q.county)) for q in query]
#     uf_unaccented_lower = unaccent(sa.func.lower(Exsiccata.state_province)).in_(list_uf)
#     state_unaccented_lower = unaccent(sa.func.lower(Exsiccata.state_province)).in_(list_state)
#     county_unaccented_lower = unaccent(sa.func.lower(Exsiccata.county)).in_(list_county)
#
#     return state_unaccented_lower, uf_unaccented_lower, county_unaccented_lower
#
#
# def table_is_empty(query):
#     return query == 0


def close(engine, session):
    engine.dispose()
    session.close()


def class_has_tablename(cls):
    return '__tablename__' in dir(cls)


def get_classes(filename: str = 'models'):
    return inspect.getmembers(importlib.import_module(filename), inspect.isclass)
