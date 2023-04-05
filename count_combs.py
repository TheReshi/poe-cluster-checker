import json

def count_combs(jewel_size):
    with open("data/clustercombs/" + jewel_size.lower() + ".json", 'r') as infile:
        cluster_data = json.load(infile)

    total_combs = 0

    for cluster in cluster_data:
        total_combs += int(cluster["clusterCombCount"])

    return total_combs

# print(f"Total Medium Cluster combinations: {count_combs('Medium')}")
# print(f"Total Large Cluster combinations: {count_combs('Large')}")