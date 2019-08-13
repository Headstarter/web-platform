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
          'Verify', 'CV', 'Position']#, 'Application']


def export():
    con = sqlite3.connect('app/app_old.db')

    for table in tables:
        outfile = open('backup/production_data_' + table + '.csv', 'w')
        outcsv = csv.writer(outfile)
        cursor = con.execute('select * from ' + table)

        # dump column titles (optional)
        # print(str(len(cursor.description)))
        # outcsv.writerows([cursor.description[x] for x in range(len(cursor.description))].join(', '))
        # dump rows
        outcsv.writerows(cursor.fetchall())

    outfile.close()


def recover():
	engine = create_engine('sqlite:///app/app_new.db')
	con = engine.connect()
 
	import app.models as db_tables
	db_tables.Base.metadata.create_all(engine)

	for table in tables:
		filename = 'backup/production_data_' + table + '.csv'
		print(table, ':')
		print(filename, ':')
		print([column.key for column in db_tables.factory(table).__table__.columns])
		print([column.type for column in db_tables.factory(table).__table__.columns])
		
		types = [column.type for column in db_tables.factory(table).__table__.columns]

		with open(filename, 'r', encoding="utf8") as f:
			r = csv.reader(f, delimiter=',', quotechar='"')
			data = []
			counter = 0
			for row in r:
				counter = counter + 1
				if counter <= len(types):
					continue
				t = tuple(row)
				d = []
				for x in range(len(types)):
					print(t[x])
					d.append('')
					if t[x] == '':
						if isinstance(types[x], Integer):
							d[x] = int(0)
						elif isinstance(types[x], String):
							d[x] = str('')
						elif isinstance(types[x], Boolean):
							d[x] = bool(True)
					else:
						if isinstance(types[x], Integer):
							d[x] = int(t[x])
						elif isinstance(types[x], String):
							d[x] = str(t[x])
						elif isinstance(types[x], Boolean):
							d[x] = bool(t[x])
				data.append(tuple(d))
				
			print(data)
			import sqlalchemy
			ins = sqlalchemy.sql.expression.insert(db_tables.factory(table), data, bind=engine)
			#print('------------------------\n', str(ins), '\n', ins.compile().params)
			con.execute(ins)

def exportOut(name):
    con = sqlite3.connect('app/' + name)

    for table in tables:
        cursor = con.execute('select * from ' + table)

        # dump column titles (optional)
        # print(str(len(cursor.description)))
        # outcsv.writerows([cursor.description[x] for x in range(len(cursor.description))].join(', '))
        # dump rows
        print(cursor.fetchall())

    #outfile.close()


# recover()
# exportOut('app_new.db')