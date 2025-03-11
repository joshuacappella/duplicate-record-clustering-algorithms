import mariadb
import sys
from tabulate import tabulate

# ESTABLISHING CONNECTION --------------------------------------------------------------

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

# Create cursor: way to send commands to the database
mycursor = conn.cursor()

# Switch to the Database used for connections
mycursor.execute("use Kardia_DB;")

fields = [
  ["p_partner.p_partner_key", "key"],
  ["p_partner.p_title", "title"],
  ["p_partner.p_preferred_name", "preferred name"],
  ["p_partner.p_surname", "surname"],
  ["p_partner.p_org_name", "org name"],
  ["p_partner.p_gender", "gender"],
  ["p_contact_info.p_contact_type", "contact type"],
  ["p_contact_info.p_phone_area_city", "phone city"],
  ["p_contact_info.p_contact_data", "contact data"],
  ["p_location.p_address_1", "address1"],
  ["p_location.p_address_2", "address2"],
  ["p_location.p_address_3", "address3"],
  ["p_location.p_city", "city"],
  ["p_location.p_state_province", "state"],
  ["p_location.p_country_code", "country"],
  ["p_location.p_postal_code", "postal code"],
]
attributes = map(lambda x: x[0], fields)
labels = map(lambda x: x[1], fields)

# INDEXING SECTION ---------------------------------------------------------------------

# Use the mysql SHOW TABLES command and print output
mycursor.execute("Show tables;")

# Print all results.
for result in mycursor.fetchall():
  print(result)


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
