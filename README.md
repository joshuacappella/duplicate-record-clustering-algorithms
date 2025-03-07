# Duplicate_Record_Clustering_Algorithms
March 2025 LightSys Code-a-thon Week 1 Codeathon Team SnowFun.

The goal of this project was to find duplicate entries in Kardia's database after the duplicate entries have already been made in less complexity than O(n<sup>2</sup>) time.

Kardia is project by LightSys, which you can read about here:
https://lightsys.org/?page=Kardia+and+Centrallix

To find duplicates, each database entry has its properties such as first name, last name, or email address clustered with other entries which have properties which are similar. Three approaches were explored to perform this clustering:
1. Storage and retrieval of properties using a trie a fixed number of characters deep. Read more at: https://en.wikipedia.org/wiki/Trie
2. Double metaphone, which groups properties together based on their phonetic pronunciations. This works best for properties which have pronunciations, such as first and last names. Read more at: https://en.wikipedia.org/wiki/Metaphone#Double_Metaphone
3. MinHash, which groups similar strings together based on how much they have in common. Read more at: https://en.wikipedia.org/wiki/MinHash

After all the database entries have had their properties grouped together, pairs of entries with two or more shared property clusters are identified for doing a more exhaustive comparison to identify duplicates. The algorithm that was chosen to perform this synthesis of properties between database entries is a variation of the Highly Connected Subgraphs (HCS) algorithm. Read more at: https://en.wikipedia.org/wiki/HCS_clustering_algorithm
