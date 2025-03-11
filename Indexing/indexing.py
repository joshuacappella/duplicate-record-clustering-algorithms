import mariadb
import sys
import numpy as np
import hashlib
from numpy.linalg import norm
from tabulate import tabulate
# Current dependencies that must be installed in order to run this script:
#   pip install numpy
#   pip install mariadb
#   pip install hashlib
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

#make vectors out of a hashed value from the phone number
def phone_number_to_hashed_vector(phone, matrix_shape=(16,1)):
    hashed_number = hashlib.sha256(phone.encode()).hexdigest()
    numerical_hash = int(hashed_number, 16)
    total_elements = matrix_shape[0] * matrix_shape[1]
    matrix_values = [(numerical_hash >> i) & 1 for i in range(16)]
    matrix = np.array(matrix_values)
    return matrix

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

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
# mycursor.execute(f"""
# SELECT {",".join(attributes)}
# FROM p_partner
# JOIN p_location     ON p_partner.p_partner_key = p_location.p_partner_key
# JOIN p_contact_info ON p_partner.p_partner_key = p_contact_info.p_partner_key
# WHERE p_partner.p_partner_key = 80965;
# """)

mycursor.execute(
"""SELECT p_partner.p_partner_key,
       GROUP_CONCAT(CONCAT(p_phone_area_city, '-', p_contact_info.p_contact_data) SEPARATOR ', ') 
AS contact_details 
FROM p_partner 
LEFT JOIN p_contact_info
ON p_partner.p_partner_key = p_contact_info.p_partner_key 
WHERE p_contact_info.p_contact_type = 'C' 
OR p_contact_info.p_contact_type = 'P'
AND p_contact_info.p_phone_area_city != ""
GROUP BY p_partner.p_partner_key;"""
)

rows = []
for data in mycursor.fetchall():
  columns = []
  for entry in data:
    columns.append(entry)
  columns.append(phone_number_to_hashed_vector(entry[1]))
  rows.append(columns)

rows = sorted(rows, key=lambda x: (x[2][0], x[2][1], x[2][2], x[2][3], x[2][4], x[2][5], x[2][6]))

for x in list(range(5)):
   print(f"{rows[x]} \n")

#print(tabulate(rows, headers=labels, tablefmt="grid"))

# Close the connection.
conn.close()
