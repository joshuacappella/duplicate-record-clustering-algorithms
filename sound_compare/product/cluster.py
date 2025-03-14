''' ----------------------------------------------------------------------------------
* FILE: cluster.py
* AUTHOR: Cody Clair, Tim Hewale, Benjamin Small
* DATE CREATED: 3/13/2025
* LAST MODIFIED: 3/14/2025
* PURPOSE: This script clusters data from a MariaDB database using the Metaphone 
  algorithm to group similar-sounding names efficiently. It retrieves data from 
  the p_partner_metaphone_surname table in the Kardia_DB database and applies a 
  custom clustering method based on predefined Metaphone prefixes.
---------------------------------------------------------------------------------- '''

import time     # For calculating computation time.

# The following funtion, grab_clusters(cursor, table_name) has one purpose:
# Given a table with indexes of users in the p_partner table, along with the 
# metaphoned value of one of the users data (ex: perferred_name, given_name, etc.),
# it will cluster based on the first three letters of the metaphone. 
# This should put fairly similar sounding words into the same clusters. 
# 
# Desired inputs include a cursor for communication with MariaDB, and the table to 
# select the metaphone values from.
# Outputs time spent and the clusters. 

def grab_clusters(cursor, table_name):
  # Start timer for grabbing the data 
  start = time.time()

  # Storage for clusters and alphabet
  clusters = []
  alphabet = ['AAAAFZ', 'AGAAMZ', 'ANAAZZ', 'BAABZZ', 'CAACZZ', 'DAADZZ', 'EAAEZZ',
              'FAAFZZ', 'GAAGZZ', 'HAAHZZ', 'IAAIZZ', 'JAAJLZ', 'JMAJNZ', 'JOAJZZ',
              'KAAKNZ', 'KOAKZZ', 'LAALZZ', 'MAAMKZ', 'MLAMZZ', 'NAANZZ', 'OAAOZZ', 
              'PAAPZZ', 'QAAQZZ', 'RAARMZ', 'RNARZZ', 'SAASLZ', 'SMASZZ', 'TAATMZ', 
              'TNATZZ', 'UAAUVV', 'VAAVZZ', 'WAAWZZ', 'XAAXZZ', 'YAAYZZ', 'ZAAZZZ']

  # We iterate for each value and sort it by the second character in the metaphone
  # Loop through a predefined list of alphabetical characters
  # Execute SQL query using f-string formatting
  # Fetch all results returned by the query
  for x in alphabet:
    cursor.execute(f"""SELECT `index` FROM {table_name} WHERE metaphone BETWEEN '{x[0:3]}%'  
    AND '{x[3:6]}%' ORDER BY SUBSTRING(metaphone, 2, 1)""")
    data = cursor.fetchall()

    #data.append(len(data))
    clusters.append(data)

  '''
  # This following section is intended to split clusters into smaller batches after the 
  # original storing of them. This is done by breaking up any cluster that is more than 
  # 100 ids. 
  # Currently commented out to make sure not spliting between possible duplicates with 
  # very similar metaphone values.
  for x in range(len(clusters)):
    if len(clusters[x]) > 100:
      temp = clusters[x]
      clusters.remove(clusters[x])
      lengthdiv = int(len(temp)/2)
      clusters.append(temp[0:lengthdiv+1])
      clusters.append(temp[lengthdiv+1:lengthdiv*2])
    #if x != []:
      #print(clusters[x])
  '''

  # Output time spent and return created clusters.
  end = time.time()
  print("FINISED CREATING CLUSTERS.")
  print("TIME SPENT: ", (end-start), "secs")
  return clusters
  
