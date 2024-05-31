from typing import Any


def insert(data: Any, session):
    try:
        session.add(data)
        session.commit()
    except:
        session.rollback()


def inserts(data: list, session):
    try:
        session.adds(data)
        session.commit()
    except:
        session.rollback()
