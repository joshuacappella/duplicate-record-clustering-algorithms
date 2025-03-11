import mariadb
import sys
from tabulate import tabulate

# Establish connection to MariaDB server

# When running this script on a local machine, you need to port forward the
# database to your local machine. You can do this using the VSCode ports menu
# if you have an open SSH menu, or by running the command below:
# Database Port Forwarding:  ssh -L 3306:localhost:3306  devel@10.5.193.178

# Create a connection to the database.
try:
  conn = mariadb.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="")
except mariadb.Error as e:
  print(f"Error connecting to the database: {e}")
  sys.exit(1)

# Create a database cursor.
mycursor = conn.cursor()
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

# Run a simple query.
mycursor.execute(f"""
SELECT {",".join(attributes)}
FROM p_partner
JOIN p_location     ON p_partner.p_partner_key = p_location.p_partner_key
JOIN p_contact_info ON p_partner.p_partner_key = p_contact_info.p_partner_key
WHERE p_partner.p_partner_key = 80965;
""")

rows = []
for data in mycursor.fetchall():
  columns = []
  for entry in data:
    columns.append(entry)
  rows.append(columns)

print(tabulate(rows, headers=labels, tablefmt="grid"))

# Close the connection.
conn.close()
