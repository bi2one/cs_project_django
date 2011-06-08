#ALTER DATABASE MyDb CHARACTER SET utf8;
#ALTER TABLE MyTable CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
from MySQLdb import *

host='localhost'
user='scm'
password='scm'
database='scm_database'

db = connect(host, user, password, database)
cursor = db.cursor()

cursor.execute('ALTER DATABASE ' + database + ' CHARACTER SET utf8')

sql = 'show tables'
cursor.execute(sql)
tables = cursor.fetchall()

for table in tables :
    cursor.execute('ALTER TABLE ' + table[0] + ' CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci')

db.close()
