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

# Switch to the Database used for connections
mycursor.execute("use Kardia_DB;")

# Get all tables.
mycursor.execute("Show tables;")

# Print all results.
for result in mycursor.fetchall():
  print(result)


print("\n")

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
