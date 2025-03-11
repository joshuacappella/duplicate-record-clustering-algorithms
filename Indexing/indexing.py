import mariadb
import sys

# ESTABLISHING CONNECTION --------------------------------------------------------------

# Establish connection to MariaDB server
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

# Create cursor: way to send commands to the database
mycursor = conn.cursor()

# Switch to the Database used for connections
mycursor.execute("use Kardia_DB;")


# INDEXING SECTION ---------------------------------------------------------------------

# Use the mysql SHOW TABLES command and print output
mycursor.execute("Show tables;")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)


print("\n")

# Use the mysql command to grab a single user and print output
mycursor.execute("SELECT * FROM p_partner WHERE p_partner_key = \"86869\";")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)


print("\n")

# Use the mysql command to grab the names and print output
mycursor.execute("desc p_partner;")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)


# Grab a list of names
contacts = []
mycursor.execute("SELECT p_partner_key, p_given_name, p_surname FROM p_partner;")
for (key, name, surname) in mycursor:
  contacts.append(f"{key} {name} <{surname}>")
print("\n".join(contacts))


conn.close()