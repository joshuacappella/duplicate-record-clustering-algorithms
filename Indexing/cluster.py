import mariadb      # Library for connecting to and modifying a MariaDB database. 
import sys          # Library for sending accurate error codes.
from metaphone import doublemetaphone

#p_partner_metaphone_test

try:
  # Assumes that a connection is available to the server on local port 3306
  conn = mariadb.connect(host="127.0.0.1", port=3306, user="root", password="")
except mariadb.Error as e:
  print(f"Error connecting to the database: {e}")
  sys.exit(1)

# creates the cursor that we can use to sumbit queries to the MariaDB
mycursor = conn.cursor()
# switches to the correct database where our test data is stored
mycursor.execute("use Kardia_DB;")
# END CONNECTION SETUP ---------------------------------------------------------------

clusters = []
alphabet = ['AAAAFZ', 'AGAAMZ', 'ANAAZZ','BAABZZ','CAACZZ','DAADZZ','EAAEZZ','FAAFZZ','GAAGZZ','HAAHZZ','IAAIZZ',
            'JAAJLZ','JMAJNZ','JOAJZZ','KAAKNZ', 'KOAKZZ', 'LAALZZ', 'MAAMKZ', 'MLAMZZ', 'NAANZZ', 'OAAOZZ', 'PAAPZZ', '', 'Z']

#We iterate for each value and sort it by the second metaphone element
for x in alphabet:
    mycursor.execute(f"""SELECT p_preferred_name, metaphone FROM p_partner_metaphone_test WHERE metaphone BETWEEN '{x[0:3]}%'  
    AND '{x[3:6]}%' ORDER BY SUBSTRING(metaphone, 2, 1)""")
    data = mycursor.fetchall()
    clusters.append(data)


for x in clusters:
   if x != []:
     print(x)
   
    
