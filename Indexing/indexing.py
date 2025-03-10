import mariadb
import sys

#Establish connection to MariaDB server
try:
  conn = mariadb.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="")
except mariadb.Error as e:
  print(f"Error connecting to the database: {e}")
  sys.exit(1)


mycursor = conn.cursor()
 
mycursor.execute("use Kardia_DB;")
mycursor.execute("Show tables;")
 
myresult = mycursor.fetchall()
 
for x in myresult:
  print(x)


conn.close()