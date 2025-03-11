# Code-A-Thon Week 2 2025



## Ben, Cody, Israel, Tim



# Problem
We need to efficently detect possible duplocates which can be presented to the user for resolution. The cosine similarity algorithm is great for determining when two peices of text are similar.

## Naive, Ideal Solution
For every record, we could go through each relevant attribute and cosine compare it to every other record to detect similar records which may be duplocates. While this solution *will* find each duplocate, it's very slow on a large amount of data (think milions of entries) because it has O(n<sup>2</sup>) complexity.

## Current Solution
The current solution sorts each relevant attribute (optimized with an index). Then, for each entry, it compares that entry to the next few entries (usually 10). This solution is far faster, however, it misses many duplocates. For example, "John" and "JJohn" (an obvious typo) will sort far appart, and this duplocate will not be detected.

## Proposed Solution
Our proposed solution (the "vector" solution) selects the the relevant attributes and computes the hashed vector for each of them individually. Then, we store these hashed vectors in a new table (see below).


| p_key | README |
| ------ | ------ |

## Relevant Attributes
We chose to examine each person's first name, last name (surname), address, email, and phone number.

### Selecting data
- First name: Select p_preferred_name from p_partner. If it's missing, select given_name from p_partner.
- Surname: Select p_surname from p_partner.
- Address: Select p_address_1, p_address_2, p_address_3, p_city, p_state_province, p_country_code, and p_postal_code from p_location. (join p_partner on p_partner_key)
- Email: Select p_contact_info from p_location where p_contact_type = "E". (join p_partner on p_partner_key)
- Phone Number: Select p_phone_area_city and p_contact_info from p_location where p_contact_type = "C" or p_contact_type = "P". (join p_partner on p_partner_key)
