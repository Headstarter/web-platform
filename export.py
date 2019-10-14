import sqlite3
import csv

con = sqlite3.connect('app/app.db')

for table in ['User', 'Mapper', 'Tag', 'Company', 'Verify', 'CV', 'Position', 'School', 'Approval']:
    outfile = open('csv/' + table + '.csv', 'w')
    outcsv = csv.writer(outfile)
    cursor = con.execute('select * from ' + table)

    # dump column titles (optional)
    outcsv.writerow(x[0] for x in cursor.description)
    # dump rows
    outcsv.writerows(cursor.fetchall())

outfile.close()
