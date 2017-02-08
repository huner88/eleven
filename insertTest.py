import MySQLdb
#Ask me for the userName and password
conn = MySQLdb.connect("*************")
x = conn.cursor()

try:
   x.execute("""INSERT INTO testTable VALUES (%s,%s,%s,%s)""",(2,2,2,2))
   conn.commit()
except:
   conn.rollback()
conn.close()
