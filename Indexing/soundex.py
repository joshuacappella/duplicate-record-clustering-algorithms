''' ----------------------------------------------------------------------------------
* FILE: soundex.py
* AUTHOR: Benjamin Small, Tim Hewale
* DATE: 3/11/2025
* PURPOSE: Implementation of the ability to sort the indexes of the p_partner table 
* based on a soundexed value. Ex. Sort the p_partner table based on soundex of the 
* given name.
---------------------------------------------------------------------------------- '''

import mariadb
import sys

# CONNECTION TO THE MARIADB on KARDIA-VM ---------------------------------------------
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



# CREATE SOUNDEX for TABLE VALUES ----------------------------------------------------

# The following function, get_soundex(cursor, table, value), does four actions:
# Create a table to store the value, soundex of the value, and the {table}_key.
# Insert all the entries from the table into the new table.
# Create an index on the soundexed value.
# Then return the table from lowest to highest soundex.
# 
# The function needs to take in three values:
# The cursor for communication with MariaDB.
# The table that would like to be selected.
# Then the table value that you would like to compute the soundex on.
#
# The returned output is a list of [<id>, <value>, <soundexed_value>]
# 
# NOTES:
# The following program will only work for tables where the primary key is a CHAR(10)
# value, and is named <table-name>_key. It will also only work for values that are of
# type VARCHAR(64).

def get_soundex(cursor, table, value):
  # create the name for the testing table (CAREFUL TO MAKE SURE THIS IS DIFFERENT 
  # THAN EXISTING TABLE NAMES)
  temp_table = f"{table}_soundex_test"

  # Destroy the table if in already exists : this could cause errors if there is 
  # a table in truly in use with the same name. 
  cursor.execute(f"""DROP TABLE IF EXISTS {temp_table};""")

  # CREATE THE TABLE in the MariaDB.
  # We want to do this to utilize the databases incorporated indexing and sorting 
  # feature.
  cursor.execute(f"""
  CREATE TABLE IF NOT EXISTS {temp_table} (
    `index` CHAR(10) PRIMARY KEY,
    {value} VARCHAR(64),
    soundex VARCHAR(255),
    FOREIGN KEY (`index`) REFERENCES {table}({table}_key)
  );
  """)

  # Inserts the table data selected into the new table. This includes the soundex of
  # the value.
  cursor.execute(f"""             
  INSERT INTO {temp_table} (`index`, {value}, soundex)
  SELECT 
    {table}_key, 
    {value}, 
    SOUNDEX({value})
  FROM 
    {table};
  """)
  
  # Possible feature to create an index on the soundex within the table. 
  # Not selected currently since table is removed after use. 
  # cursor.execute(f"""CREATE INDEX soundex_index ON {temp_table}(soundex);""")

  # Order and save the output by the ascending soundex.
  cursor.execute(f"""SELECT * FROM {temp_table} ORDER BY soundex;""")
  data = cursor.fetchall()

  # Deletes the table then returns the data.
  cursor.execute(f"""DROP TABLE IF EXISTS {temp_table};""")
  return data


# test query to grab perferred name from the p_partner table. 
items = get_soundex(mycursor, "p_partner", "p_preferred_name")
for x in items:
  print(x)


# CLOSE CONNECTION TO SERVER ---------------------------------------------------------
conn.close()
# END CLOSE CONNECTION ---------------------------------------------------------------
