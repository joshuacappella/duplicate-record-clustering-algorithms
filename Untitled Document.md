# Code-A-Thon Week 2 2025



## Ben, Cody, Israel, Tim



# Problem
We need to efficently detect possible duplocates which can be presented to the user for resolution. The cosine similarity algorithm is great for determining when two peices of text are similar.

## Naive, Ideal Solution
For every record, we could go through each relevant attribute and cosine compare it to every other record to detect similar records which may be duplocates. While this solution *will* find each duplocate, it's very slow on a large amount of data (think milions of entries) because it has O(n<sup>2</sup>) complexity.

## Current Solution
The current solution sorts each relevant attribute (optimized with an index). Then, for each entry, it compares that entry to the next few entries (usually 10). This solution is far faster, however, it misses many duplocates. For example, "John" and "JJohn" (an obvious typo) will sort far appart, and this duplocate will not be detected.


## Solutions that Have been Attempted and Deadended
   In our attempts to find efficient clustering and/or sorting algorithms, we have tried and failed the following approaches:
 - The previous teams solution, using MinHash and Clusters based on a particular Python library. We decided this approach was too poorly documented to be built off of and could be done better.
 - Simple vector sorting: Due to the impossibility of properly sorting vectors by elements within the vector, since no one element is *seemingly* more important than another. Thus, the concept of sorting by vector elements and keeping the sliding window approach is unfeasible.

## Sliding Window
   The sliding window is essentially the way that the cosine algorithm checks for duplicates. The concept will continue to be used for this step of duplicate checking. The sliding window checks a number of sorted records below it for each record (e.g. a window of 50 records) by using the cosine algorithm and presents it as a duplicate if the cosine value is close enough to 1.0 (identical)

## Proposed Solution
Our proposed solution has two parts that we would like to ideally combine, applying one of these functions to each attribute we desire to check. 
   1. One computes the hashed vector for each of them individually, in the same way that it is done to check the cosine value in the sliding window technique listed above. Then, we store these hashed vectors in a new table (see below)
   This approach is more helpful for the following types of duplicates:
         - Duplicates where names are different but phone numbers could be the same
         - Where the emails are the same or similar but the last name changed (marriage)
         -   Others where typical names are very unalike

2. The other would take in a string (perhaps, `p_given_name` or `p_preferred_name`) and compute a metaphone or `SOUNDEX` value to try to find strings that sound similar. This method will be better at clustering duplicates that have:
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
