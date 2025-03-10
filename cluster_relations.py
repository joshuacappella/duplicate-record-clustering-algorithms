# EXAMPLE: The purpose of this file is to demonstrate a simple
    # example of how to take the properties created from each
    # algorithm and select only the entries that show up in
    # multiple clusters of [multiple algorithm's property dictionaries]
    # The ChatGPT prompt that suggested this comparison method was
    # (we think) partially inspired by something made in the 2000s
    # called the [H]ighly-[C]onnected [S]ubgraphs Clustering Algorithm.
    # We do not actually follow that algorithm. We came up with
    # portions of this based on the needs of our problem and it
    # doesn't form a graph at the end. The HCS Clustering Algorithm
    # could be worth looking into

# Assumes each algorithm creates a property cluster list/HashMap 
# of lists. Each list contains the indices of the entries
# that were clustered together with that algorithm

# Example maps implemented as dictionaries in python
firstPropertyDictionary = {0: [1,2,3], 1: [1,2], 2: [1,3,4,5]}
# secondPropertyDictionary = {1: [2,4], 2: [3,5], 3: [1]}
# thirdPropertyDictionary = {1: [1,3], 2: [5], 3: [4]}

# determine threshold for how many properties two entries need to have in common to be considered duplicates 
threshold = 2
savedGroupedPairs = []

## call each map and operate on each list 
# For each key of the map, operate on the list by creating a map to count associations for each entry.
# the keys for this association map should [contain] the IDs of each entry

propertyAssociations = {0: [0,0,0,0,0,0], 1: [0,0,0,0,0,0], 2: [0,0,0,0,0,0], 3: [0,0,0,0,0,0], 4: [0,0,0,0,0,0], 5: [0,0,0,0,0,0]}

# For each index within the list
for key in firstPropertyDictionary:
    currentPropertyCluster = firstPropertyDictionary[key]

    #   If list.length > 1, loop through the list, declaring the current index the target 
    if len(currentPropertyCluster) > 1:
        for i, entryID in enumerate(currentPropertyCluster):
            target = entryID
            targetAssociationList = propertyAssociations[target]

            #	For each index after target 
            for j, nextID in enumerate(currentPropertyCluster[i:]):
                if nextID == target:
                    # Don't check yourself bruh
                    dontCheckTheTarget = True

                #   Increment the respective association counter for the association list entry for the
                #   given index (since every index that comes after the target is already in the same
                #   currentpropertyCluster list, we need to report that this index has already been found
                #   to have one property in common with the target. We do this by incrementing the index's 
                #   value in the target's targetAssociationList)
                else:
                    targetAssociationList[nextID] += 1

                    # 	If counter of given index is now == threshold, group this index with the target by
                    #   saving the pair (target, index we’re currently on after the target)
                    #   to the final list of pairs
                    if targetAssociationList[nextID] == threshold:
                        savedGroupedPairs.append((target,nextID))

    #   If list.length == 1 or other, do nothing, 
    else:
        doNothing = True

## CHOOSE:
# Either do the same process for secondPropertyDictionary and thirdPropertyDictionary and so on...
# OR concatenate the clusterPropertyCluster lists of all propertyDictionaries together for each property/algorithm
# used to create the clustered inputs and run through all of them in sequence (Concatenation might be more efficient?)

# ...

# Return the final clustered pairs (this could be improved to order the pairs in a specific way rather than in
# the default order as a result of appending during the iterations)
print("Results: ", savedGroupedPairs)
