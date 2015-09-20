import sqlite3

file_db = 'test_sqlite3.db'
conn = sqlite3.connect(file_db)


# Create a cursor object and call execute to perform commands
c = conn.cursor()

# Create table
#c.execute('''CREATE TABLE inventory
#             (date text, macro_name text, arg real)''')

# Insert a row of data
c.execute("INSERT INTO inventory VALUES ('2015-04-05','mxraster',4)")

# Save (commit) the changes
conn.commit()

for row in c.execute('SELECT * FROM inventory ORDER BY macro_name'):
    print row


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
