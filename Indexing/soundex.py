import mariadb
import sys

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

  cursor.execute(f"""             
  SELECT * FROM {temp_table} ORDER BY soundex;
  """)

  data = cursor.fetchall()

  cursor.execute(f"""DROP TABLE IF EXISTS {temp_table};""")

  return data



items = get_soundex(mycursor, "p_partner", "p_preferred_name")
for x in items:
  print(x)

# Close the connection.
conn.close()
