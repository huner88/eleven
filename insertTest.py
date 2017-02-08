import MySQLdb
conn = MySQLdb.connect("128.199.137.57","shiyiqun","shiyiqun","test")
x = conn.cursor()

try:
   x.execute("""INSERT INTO testTable VALUES (%s,%s,%s,%s)""",(2,2,2,2))
   conn.commit()
except:
   conn.rollback()
conn.close()