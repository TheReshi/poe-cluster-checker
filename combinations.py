import resources as res
import json
import itertools

def generate_combinations(jewel_size):
    all_comb = []
    with open("data/clustermods/" + jewel_size.lower() + ".json", 'r') as infile:
        cluster_data = json.load(infile)

    for cluster in cluster_data:
        # print(cluster["clusterPrefixes"])

        if jewel_size.lower() == "large":
            cluster_combs = []

            prefix_combs = [list(x) for x in itertools.combinations(cluster["clusterPrefixes"], 2)]

            for suffix in cluster["clusterSuffixes"]:
                cluster_combs += [x + [suffix] for x in prefix_combs]

            # print(list(combs))
        elif jewel_size.lower() == "medium":
            cluster_combs = [list(x) for x in itertools.combinations(cluster["clusterPrefixes"], 2)]
        else:
            cluster_combs = cluster["clusterPrefixes"]

        print(cluster_combs)

        cluster_info = {
            'clusterId': cluster["clusterId"],
            'clusterName': cluster["clusterName"],
            'clusterCombCount': len(cluster_combs),
            'clusterCombs': cluster_combs
        }

        all_comb.append(cluster_info)

    return all_comb

# asd = generate_combinations("Large")
def update_comb_data():
    with open('data/clustercombs/large.json', 'w') as outfile:
        json.dump(generate_combinations("Large"), outfile, indent=2)

    with open('data/clustercombs/medium.json', 'w') as outfile:
        json.dump(generate_combinations("Medium"), outfile, indent=2)

    with open('data/clustercombs/small.json', 'w') as outfile:
        json.dump(generate_combinations("Small"), outfile, indent=2)