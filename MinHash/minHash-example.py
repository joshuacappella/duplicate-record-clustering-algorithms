from datasketch import MinHash, MinHashLSH
from itertools import combinations
import csv

NUM_PERM=128
THRESHOLD=0.4

# Load sample list of near-duplicate strings
rows = []
with open("./sample-data/test.csv") as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    rows = [r for r in csvreader]

# Filter rows to the properties we actualy want to use
cData = [r[7:11] for r in rows]

def shingle(text: str, k: int):
    shingle_set = []
    for i in range(len(text) - k+1):
        shingle_set.append(text[i:i+k])
    print(shingle_set)
    return set(shingle_set)

# Function to create a MinHash signature for a row in the database (row is a python list)
def get_minhash(row):
    minhash = MinHash(num_perm=NUM_PERM)
    for shinglePiece in shingle(" ".join(row), 2):
        minhash.update(shinglePiece.encode('utf8'))
    return minhash

# Create an empty LSH index (hash map)
lsh = MinHashLSH(threshold=THRESHOLD, num_perm=NUM_PERM)

# Compute hashes storing them in the lsh index. Also store the items in a dictionary with their hashes to be able to look them up in the lsh index when returning results
minhash_dict = {}
for i, row in enumerate(cData):
    minhash = get_minhash(row)
    lsh.insert(f"row_{i}", minhash)  # Insert into LSH index
    minhash_dict[f"row_{i}"] = (row, minhash)

# Group near-duplicates by querying LSH
clusters = []
visited = set()

csvData = []
for key, (doc, minhash) in minhash_dict.items():
    if key not in visited:
        # Find similar documents
        similar_docs = lsh.query(minhash)
        clusters.append([cData[int(doc_id.split("_")[1])] for doc_id in similar_docs])
        visited.update(similar_docs)
# Output the near-duplicate clusters
for i, cluster in enumerate(clusters):
    if (len(cluster) > 1) :
        #print(f"{cluster}: {len(cluster)}")
        for item in cluster:
            csvData.append(item)
            print(item[0], end=", ")
        print(len(cluster))
        csvData.append([len(cluster)])

print(len(clusters))

# output data to be easily read from excel to see how the algorithm did
with open("sample-data/test-out.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csvData)

