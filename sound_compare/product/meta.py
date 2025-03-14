''' ----------------------------------------------------------------------------------
* FILE: metaphone.py
* AUTHOR: Benjamin Small, Tim Hewale
* DATE CREATED: 3/11/2025
* LAST MODIFIED: 3/13/2025
* PURPOSE: Implementation of the ability to sort the indexes of the p_partner table 
* based on a double metaphoned value. Ex. Sort the p_partner table based on double 
* metaphone of the given name.
---------------------------------------------------------------------------------- '''

import time
from metaphone import doublemetaphone

# CREATE METAPHONE for TABLE VALUES --------------------------------------------------

# The following function, get_metaphone(cursor, table, value), does four actions:
# Create a table to store the value, metaphone of the value, and the {table}_key.
# Insert all the entries from the table into the new table.
# Create an index on the metaphoned value.
# Then return the table from lowest to highest metaphone.
# 
# The function needs to take in three values:
# The cursor for communication with MariaDB.
# The table that would like to be selected.
# Then the table value that you would like to compute the metaphone on.
#
# The returned output is a list of [<id>, <value>, <metaphoned_value>]
# 
# NOTES:
# The following program will only work for tables where the primary key is a CHAR(10)
# value, and is named <table-name>_key. It will also only work for values that are of
# type VARCHAR(64).

def get_metaphone(conn, cursor, out_table, table, value):
  start = time.time()

  # create the name for the testing table (CAREFUL TO MAKE SURE THIS IS DIFFERENT 
  # THAN EXISTING TABLE NAMES)
  temp_table = f"{out_table}"

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
    metaphone VARCHAR(255),
    FOREIGN KEY (`index`) REFERENCES {table}({table}_key)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
  """)

  # Inserts the table data selected into the new table. This includes the metaphone 
  # of the value. 
  # Grab all of the keys and values for each entry into the table
  cursor.execute(f"""SELECT {table}_key, {value} FROM {table} WHERE {value} != '';""")
  data = cursor.fetchall()

  # Go through and one by one insert the values into the new table. 
  for row in data :
    primary_key = row[0]
    og_value = row[1]
    dm_value = doublemetaphone(og_value)[0]

    cursor.execute(f"""
    INSERT INTO {temp_table} (`index`, {value}, metaphone)
    VALUES (%s, %s, %s);
    """, (primary_key, og_value, dm_value))
  
  
  # Possible feature to create an index on the metaphone within the table. 
  # Not selected currently since table is removed after use. 
  # cursor.execute(f"""CREATE INDEX metaphone_index ON {temp_table}(metaphone);""")

  # Order and save the output by the ascending metaphone.
  cursor.execute(f"""SELECT * FROM {temp_table} ORDER BY metaphone;""")
  data = cursor.fetchall()

  # Deletes the table then returns the data.
  # cursor.execute(f"""DROP TABLE IF EXISTS {temp_table};""")
  conn.commit()
  end = time.time()
  print("FINISED COMPLETING TABLE: ", {temp_table})
  print("TIME SPENT: ", (end-start), "secs")
  return data









# UNUSED CODE ------------------------------------------------------------------------
# Attempt to speed up code, but ultimately was slower. 
'''
  # THE FOLLOWING SECTION TRIED TO IMPLEMENT THIS BY GRABBING ONE ROW FROM TABLE
  # INSERTING THE METAPHONE, THEN MOVING TO NEXT ROW. THIS ULTIMATELY PROVED TO BE 
  # SLOWER. 

  cursor.execute(f"""
    SELECT {table}_key 
    FROM {table} 
    WHERE {value} != '' 
    ORDER BY {table}_key;
  """)
  primary_keys = cursor.fetchall()

  for (primary_key,) in primary_keys :
    data_cursor = conn.cursor()
    data_cursor.execute(f"""
      SELECT {value} 
      FROM {table} 
      WHERE {table}_key = {primary_key};
    """)
    
    og_value = data_cursor.fetchall()
    og_value = og_value[0][0]
    dm_value = doublemetaphone(og_value)[0]

    cursor.execute(f"""
    INSERT INTO {temp_table} (`index`, {value}, metaphone)
    VALUES ({primary_key}, '{og_value}', '{dm_value}');
    """)
  '''

