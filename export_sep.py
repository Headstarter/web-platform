import sqlite3
import csv

from numpy import genfromtxt
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import pandas as pd
from sqlalchemy import Column, Integer, String, Boolean

tables = ['User', 'Mapper', 'Tag', 'Company',
          'Verify', 'CV', 'Position', 'Application', 'School']
variables = ['_users', '_mappers', '_tags', '_companies', 
             '_verifies', '_cvs', '_offers', '_applications', 'schools', '_approvals']


def exportOut(name):
	con = sqlite3.connect('app/' + name)

	print('from app.models import db, User, Mapper, Tag, Company, Verify, CV, Position, School, Approval')

	for x in range(len(tables)):
		table = tables[x]
		var = variables[x]
		cursor = con.execute('select * from ' + table)
		print(variables[x], '=', cursor.fetchall())
        
		print('for x in', var + ':')
		print('	try:')
		print('		db.session.add(' + table + '(*x))')
		print('		db.session.commit()')
		print('	except Exception as e:')
		print('		db.session.rollback()')
		print('		print(str(e), \'\\n\', x)')


exportOut('app.db')