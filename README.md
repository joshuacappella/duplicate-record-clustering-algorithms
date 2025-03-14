# Code-A-Thon Week 2 2025



## Ben, Cody, Israel, Tim



# Problem
We need to efficently detect possible duplocates which can be presented to the user for resolution. The cosine similarity algorithm is great for determining when two peices of text are similar.

## Naive, Ideal Solution
For every record, we could go through each relevant attribute and cosine compare it to every other record to detect similar records which may be duplocates. While this solution *will* find each duplicate, it's very slow on a large amount of data (think milions of entries) because it has O(n<sup>2</sup>) complexity.

## Current Solution
The current solution sorts each relevant attribute (optimized with an index). Then, for each entry, it compares that entry to the next few entries (usually 10). This solution is far faster, however, it misses many duplocates. For example, "John" and "JJohn" (an obvious typo) will sort far appart, and this duplocate will not be detected.


## Solutions that Have been Attempted and Deadended
   In our attempts to find efficient clustering and/or sorting algorithms, we have tried and failed the following approaches:
 - The previous teams solution, using MinHash and Clusters based on a MinHash library. We realized this approach had some limitations could be done better.
 - Simple vector sorting: Due to the impossibility of properly sorting vectors by elements within the vector, since no one element is *seemingly* more important than another. Thus, the concept of sorting by vector elements and keeping the sliding window approach is unfeasible.

## Soundex 
Soundex is a phonetic algorithm that encodes words based on their pronunciation, helping to identify similar-sounding names despite differences in spelling.  
It is useful in duplicate detection by grouping names with similar phonetic representations, reducing the number of comparisons needed.  
In this project, Soundex is used to cluster records with similar-sounding attributes, improving the efficiency of duplicate detection in Kardia_DB. It ultimately didn't satisfy the scope of this project because minor typos can lead to incorrect matches– (e.g., "Pohn" instead of "John") may result in different codes, hence the implemetation of Metaphone which has more adequate funtionality for this project.  

## Sliding Window
   The sliding window is essentially the way that the cosine algorithm checks for duplicates. The concept will continue to be used for this step of duplicate checking. The sliding window checks a number of sorted records below it for each record (e.g. a window of 50 records) by using the cosine algorithm and presents it as a duplicate if the cosine value is close enough to 1.0 (identical)

## Proposed Solution
Our proposed solution has two parts that we would like to ideally combine, applying one of these functions to each attribute we desire to check. 
   1. The file in the GitHub titled `kmeans.c` is our first proposed clustering solution coded in C. It utilizes functionality implemented by the current cosine checking solution within the sliding window of vectors. The way this is improved is by using the K-means clustering algorithm to create centroids and vector points on a graph and cluster them based on which centroid point has the smallest distance from the point. Although not tested on values, an approach of this nature could be *more* helpful for the following types of duplicates:
         - Duplicates where names are different but phone numbers could be the same
         - Where the emails are the same or similar but the last name changed (marriage)
         -   Others where typical names are very unalike

2. The other approach is provided in the directory **[Indexing](https://github.com/Lightning11wins/duplicate-record-clustering-algorithms/tree/main/Indexing)**, primarily the files **[meta.py](https://github.com/Lightning11wins/duplicate-record-clustering-algorithms/blob/main/Indexing/meta.py)**, **[cluster.py](https://github.com/Lightning11wins/duplicate-record-clustering-algorithms/blob/main/Indexing/cluster.py)**, and **[compare.py](https://github.com/Lightning11wins/duplicate-record-clustering-algorithms/blob/main/Indexing/compare.py)**, and it attempts to: \
   ###### Meta.py
   1. Takes in the name of a desired test table, creates the table with an `index` (a foreign key to `p_partner_key`, the foreign key in `p_partner`, a provided field name (such as `p_surname`), and `metaphone` for the `metaphone` value of the string.
   2. For every record in the `p_partner` table, it selects the key and the desired field. For every row that it returns, it inserts into the test table (above) the key, desired field value, and the `metaphone` value of the string value. 
   ###### Cluster.py
   1. Now that we have the data in the table, we select ONLY the `index` field of each record, but select in between some substrings of clusters. Most notably, the fragment `BETWEEN '{x[0:3]}%' AND '{x[3:6]}%'` takes string `x` from `alphabet` and searches between the two substrings. For the first element of `alphabet`, the statement turns into `BETWEEN 'AAA%' AND 'AFZ%'`, or all elements with a metaphone starting from AA to AG.
   2. It does this for all substrings in `alphabet`, and for each returned query it inserts a list of tuples into an outer list `clusters`. After it does this for each element in `alphabet`, it checks the length of each cluster- if it is greater than 100, it splits into two (sometimes still larger than 100- minor bug) and returns the new list of clusters
   ###### Compare.py 
   1. From the list of lists of tuples containing the `p_partner_key`, we use the sliding window and Levenshtein distance technique to check within each cluster the FULL name (given_name + surname) with other names in the window.
   2. The result of this file prints out:
      - The time elapsed in creating the inbetween table
      - The time elapsed in creating the clusters
      - Each line follow is a printout of two values that are similar based on their Levenshtein distance. If their Levenshtein distance is from 0.75-1.0, it is listed as a possible duplicate along with their Levenshtein distance.
   
This solution is a more tested one, although it is currently only usable to check duplicate names. This solution is best implemented for the following types of duplicates:
   - misspelled name errors, which could be harder for cosine to find
   - other minor character differences
   - Metaphone also does well with differences such as "john" and "ajohn", as it can start with different letters but be sorted similarly based on the pronounciation of the rest of the word.


## Relevant Attributes
We chose to examine each person's first name, last name (surname), address, email, and phone number.

### Selecting data
- First name: Select p_preferred_name from p_partner. If it's missing, select given_name from p_partner.
- Surname: Select p_surname from p_partner.
- Address: Select p_address_1, p_address_2, p_address_3, p_city, p_state_province, p_country_code, and p_postal_code from p_location. (join p_partner on p_partner_key)
- Email: Select p_contact_info from p_location where p_contact_type = "E". (join p_partner on p_partner_key)
- Phone Number: Select p_phone_area_city and p_contact_info from p_location where p_contact_type = "C" or p_contact_type = "P". (join p_partner on p_partner_key)
