''' ----------------------------------------------------------------------------------
* FILE: input.py
* AUTHOR: Benjamin Small, Tim Hewale
* DATE CREATED: 3/13/2025
* LAST MODIFIED: 3/13/2025
* PURPOSE: Implementation of the ability to insert, delete, and show items from the 
* database. This goes along with soundex.py file, where our hopes are to check the
* soundex of foreign characters. 
* IMPORTANT: Before running the script, connect to the database with:
  ssh -L 3306:localhost:3306  devel@10.5.193.178
---------------------------------------------------------------------------------- '''

import mariadb      # Library for connecting to and modifying a MariaDB database. 
import sys          # Library for sending accurate error codes.
from datetime import datetime   # Grab date time for inserts.


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



# INSERT, DELETE, SHOW OPERATIONS ----------------------------------------------------

# The following function, insert(cursor, item, value) does two main actions:
# Grab the most recent p_partner_key.
# Insert a new user with dummy data besides the specified item (ex. p_perferred_name, 
# p_given_name). 
# 
# The purpose of the function is so we can insert new items quickly and check how well
# the soundex feature does at looking at foreign characters.
#
# The file expects the cursor, item (ex. p_perferred_name, p_given_name), and the 
# value to be inputed. This is expected to be a set of characters to form a name.
def insert(cursor, item, value):
  # Display the table from highest to lowest partner key, but only take the first one.
  cursor.execute(f"""
    SELECT p_partner_key 
    FROM p_partner 
    ORDER BY p_partner_key 
    DESC LIMIT 1;
  """)
  # Take the data, then add 1 to get the next partner id that needs to be inputed. 
  data = cursor.fetchall()
  key_val = int(data[0][0]) + 1

  # Grab current time that will be inputed. 
  now = datetime.now()
  time = now.strftime('%Y-%m-%d %H:%M:%S').replace('-0', '-')

  # Insert the new user into the table using dummy data. 
  # The only valuable data is the name for the given item type (ex. p_perferred_name, 
  # p_given_name).
  cursor.execute(f"""
    INSERT INTO p_partner (p_partner_key, 
                          p_partner_class, 
                          p_status_code, 
                          p_record_status_code, 
                          p_creating_office, 
                          {item}, 
                          s_date_created, 
                          s_created_by, 
                          s_date_modified, 
                          s_modified_by) 
    VALUES ({key_val}, 
            'IND', 
            'A', 
            'A', 
            'ben-tim', 
            '{value}', 
            '{time}', 
            'ben-tim-script', 
            '{time}', 
            'ben-tim-script');
  """)
  # This makes sure the contents are saved to the table.
  conn.commit() 


# The following function, delete(cursor, item, value) does one operation:
# Delete the selected name from p_partner. 
def delete(cursor, item, value):
  cursor.execute(f"""
    DELETE FROM p_partner WHERE {item} = '{value}';
  """)
  # This makes sure the contents are saved to the table.
  conn.commit()


# The following function, show(cursor, item) does one operation:
# Show all the items from the table p_partner, but only the item (ex. p_perferred_name, 
# p_given_name) selected. 
def show_item(cursor, item):
  cursor.execute(f"""
    SELECT {item}, p_partner_key FROM p_partner
    ORDER BY s_date_created;
  """)
  
  data = cursor.fetchall()
  for x in data:
    print(x[0])

# END OPERATIONS ---------------------------------------------------------------------



# CHOOSE OPERATIONS TO IMPLEMENT -----------------------------------------------------
def main():
  insert(mycursor, "p_preferred_name", "王大力")
  delete(mycursor, "p_preferred_name", "王大力")
  show_item(mycursor, "p_preferred_name")

# Run Main ---------------------------------------------------------------------------
if __name__=="__main__" :
  main()
  