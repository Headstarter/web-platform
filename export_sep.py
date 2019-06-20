import sqlite3
import csv

con = sqlite3.connect('app/app_old.db')

for table in ['User', 'Mapper', 'Tag', 'Company', 'Verify','CV','Position']:
	outfile = open('backup/production_data_' + table + '.csv', 'w')
	outcsv = csv.writer(outfile)
	cursor = con.execute('select * from ' + table)

# dump column titles (optional)
	print(len(cursor.description))
	outcsv.writerows([cursor.description[x] for x in range(len(cursor.description))])
# dump rows
	outcsv.writerows(cursor.fetchall())

outfile.close()
