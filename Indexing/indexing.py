import mariadb
import sys

#Establish connection to MariaDB server

# NEED TO RUN:  ssh -L 3306:localhost:3306  devel@10.5.193.178
# This creates the connection from the server for the python script to connect to.
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

print("\n")

mycursor.execute("SELECT * FROM p_partner WHERE p_partner_key = \"86869\";")
myresult = mycursor.fetchall()
 
for x in myresult:
  print(x)



conn.close()