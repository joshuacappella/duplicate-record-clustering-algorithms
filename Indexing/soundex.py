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

# The following function does four actions:
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
def get_soundex(cursor, table, value):
  temp_table = f"{table}_soundex_test"

  cursor.execute(f"""DROP TABLE IF EXISTS {temp_table};""")

  cursor.execute(f"""
  CREATE TABLE IF NOT EXISTS {temp_table} (
    `index` CHAR(10) PRIMARY KEY,
    {value} VARCHAR(64),
    soundex VARCHAR(255),
    FOREIGN KEY (`index`) REFERENCES {table}({table}_key)
  );
  """)

  cursor.execute(f"""             
  INSERT INTO {temp_table} (`index`, {value}, soundex)
  SELECT 
    {table}_key, 
    {value}, 
    SOUNDEX({value})
  FROM 
    {table};
  """)
  
  cursor.execute(f"""CREATE INDEX phonex_index ON {temp_table}(soundex);""")

  cursor.execute(f"""SELECT * FROM {temp_table} ORDER BY soundex;""")

  data = cursor.fetchall()

  cursor.execute(f"""DROP TABLE IF EXISTS {temp_table};""")

  return data


# test query to grab 
items = get_soundex(mycursor, "p_partner", "p_preferred_name")
for x in items:
  print(x)


# CLOSE CONNECTION TO SERVER ---------------------------------------------------------
conn.close()
# END CLOSE CONNECTION ---------------------------------------------------------------
