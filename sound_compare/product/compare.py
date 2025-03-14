''' ----------------------------------------------------------------------------------
* FILE: compare.py
* AUTHOR: Benjamin Small, Tim Hewale
* DATE CREATED: 3/13/2025
* LAST MODIFIED: 3/14/2025
* PURPOSE: Detect and cluster duplicate records in the Kardia_DB database using
* Metaphone and Levenshtein. It identifies the names based on their IDs and finds 
* potential duplicates efficiently using a sliding window approach.
---------------------------------------------------------------------------------- '''
import mariadb      # Library for connecting to and modifying a MariaDB database.    
import sys          # Library for sending accurate error codes.

import time         # For checking how long the algorithm takes to run.
import Levenshtein  # For a quickly implemented comparison
# (would prefer cosine, this was simple to implement)

from meta import get_metaphone      # grabs the metaphone table creation tool
from cluster import grab_clusters   # 


# CONNECTION TO THE MARIADB on KARDIA-VM ---------------------------------------------
# This connection is neccesary for using the Kardia_DB table.
# SAMPLE CODE TO HOST ON PORT 3306:
# ssh -L 3306:localhost:3306  devel@10.5.193.178
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



# DEFINITIONS AND FUNCTIONS ----------------------------------------------------------

# The following function, leven_words(name1, name2), does one simple action:
# Compare two words and return a number value that displays how similar they are using
# the levenshtein function. Would prefer cosine compare, this was simply a faster 
# implementation due to the constraints of the codathon.
#
# Desired input is two strings you wish to compare. 
def leven_words(name1, name2):
  distance = Levenshtein.distance(name1, name2)
  return 1 - (distance / max(len(name1), len(name2)))


# The following function, grab_names(cursor, id), does:
# Retrieve the given name and surname for a specific partner ID from the database and
# returns the full name as a string.
#
# The goal is so we can compare the first and last name of an individual rather than
# simply one or the other. 
#
# Desired input is the cursor for executing MariaDB commands, and a valid id from the
# p_partner table. 
def grab_names(cursor, id):
  cursor.execute(f"""
    SELECT p_given_name, p_surname FROM p_partner WHERE p_partner_key = {id};
  """)
  data = cursor.fetchall()
  return data[0][0] +  " " + data[0][1]


# The following function, sliding_window(cursor, cluster...) does:
# Given a cluster of ids, slide over the data with a given window size, and compare
# names within the window.
# 
# The expected input is a cursor to execute commands in MariaDB, a single cluster 
# (list of valid ids within the p_partner table), a window size (how many words 
# should be compared together), and the confidence value to output matches. Use a 
# number greater than or equal to 0 and less than or equal to 1. 
# 
# The expected output is a printed list of the matches above the fiven confidence
# value.  
def sliding_window(cursor, cluster, window_size, confidence_val) :
  # Go through all the ids in the cluster except the last one, since it will be 
  # compared with all before it.
  for i in range(len(cluster)-1):
    # Makes sure not to go out of bounds. Loops through the window size or the smallest
    # rest of the ids in the cluster.
    j = 0
    for k in range(min(window_size, (len(cluster)-(i+j+1)))):
      j = k
      # Call grab names on the correct cluster spots, then check similarity.
      word1 = grab_names(cursor, cluster[i][0])
      word2 = grab_names(cursor, cluster[i+k+1][0])
      sim = leven_words(word1, word2)

      # Output values above the selected confidence value.
      if sim > confidence_val :
        print("Name One: " + word1 +
              "\tName Two: " + word2 +
              "\tSim Value: " + str(sim))

# END DEFINITIONS AND FUNCTIONS ------------------------------------------------------



# MAIN FUNCTION ----------------------------------------------------------------------
# Within this we are going to grab the surnames, output the metaphone values, cluster 
# by those values, then print the matches within each cluster. 
def main():
  # Start the timer for the total computation time from start to finish.
  start = time.time()

  # Call the metaphone function to ceate a table for p_surname that saves ids, the 
  # surname, and the metaphone value of the surname.
  # Find more documentation in meta.py
  get_metaphone(conn, mycursor, "p_partner_metaphone_surname", "p_partner", "p_surname")

  # Call the clusters function to cluster the surnames based on the first three values
  # of the metaphone. This returns each element as an id.
  # Find more documentation in cluster.py
  clusters = grab_clusters(mycursor, "p_partner_metaphone_surname")

  # Loop through each cluster and output the matches with a sliding window size of 5
  # and confidence value of 0.7
  print("Possible Matches: ")
  for row in clusters:
    sliding_window(mycursor, row, 5, 0.7)

  # Print the total execution time.
  end = time.time()
  print("TOTAL EXECUTION TIME: ", (end-start), "sec")

# END MAIN FUNCTION ------------------------------------------------------------------


if __name__=="__main__" :
  main()