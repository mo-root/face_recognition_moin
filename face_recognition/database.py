from model import *
#import sqlite
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
#from IPython.core import get_ipython

# hist = get_ipython().history_manager
# hist.db = sqlite3.connect(hist.hist_file , check_same_thread = False)



engine = create_engine('sqlite:///database.db?check_same_thread=False')
Base.metadata.create_all(engine)
# session = scoped_session(sessionmaker(bind=engine))
DBSession = sessionmaker(bind=engine)
session = DBSession()


#the view is the credit card number
def add_face(name,image,description,name2):
	face_obj = Face(
		name = name,
		image = image,
		description = description,
		name2 = name2)
	session.add(face_obj)
	session.commit()

def query_by_id(face_id):
    face = session.query(Face).filter_by(face_id=face_id).first()
    return face

def delete_by_id(face_id):
	session.query(Face).filter_by(face_id=face_id).delete()
	session.commit()

def query_all():
	people = session.query(Face).all()
	return people


def update_person(person_id,name,image):
	face = query_by_id(face_id)
	if name != "":
		face.name=name
	if picture != None:
		face.image = image
	session.commit()


def query_by_name(face_name):
    nace = session.query(Face).filter_by(name=face_name).all()
    return nace


# def delete1():
#         Items = session.query(Item).all()
#         session.Item.query.delete()
#         session.commit()

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()