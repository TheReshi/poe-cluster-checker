import requests
from bs4 import BeautifulSoup
import json, os, re
import resources as res

# Initialize default headers for requests
headers = requests.utils.default_headers()

# Update header with personal info
headers.update({
    'User-Agent': "Reshi's Cluster Checker",
    'From': 'bacsadave@gmail.com'
})

# Get all the mods from the official API
response_stats = requests.get("https://www.pathofexile.com/api/trade/data/stats", headers=headers)
all_stats = response_stats.json()

# Used for determining cluster notables, returns [Notable name, Weight, Level req, Pre/Suf]
def remove_non_capital_prefixes(text):
    result = re.sub(r'^[^A-Z]*', '', text)
    return result.split(';')

def get_poedb_data(cluster_size):
    print(f"{res.BgColors.BOLD}{res.BgColors.BLUE}{cluster_size}{res.BgColors.ENDC} Cluster data fetching {res.BgColors.BOLD}{res.BgColors.GREEN}started{res.BgColors.ENDC}!")

    list_of_clusters = []

    # Get Cluster cluster data
    url = "https://poedb.tw/us/Cluster_Jewel#EnchantmentModifiers"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the main table that contains all the clusters
    cluster_table = soup.select_one('#EnchantmentModifiers > div.card.mb-2 > div.table-responsive > table > tbody')
    # Get all the cluster rows individually
    clusters = cluster_table.find_all("tr", recursive=False)

    # Go through all the clusters
    for cluster in clusters:
        # Get all 'a' tags (First element is the cluster name, last is the cluster type)
        cluster_a_tags = cluster.find_all('a')
        cluster_name = cluster_a_tags[0].get_text()
        cluster_type = cluster_a_tags[-1].get_text()

        # If there is a "del" tag, the cluster type is deleted, let's skip this loop
        if cluster.find('del') or cluster_size not in cluster_type:
            continue

        # Let's delete details if it exists in the cluster name (They are written in a "()" clause)
        if '(' in cluster_name:
            cluster_name = cluster_name.split('(', 1)[0]

        cluster_id = 0
        for i in all_stats['result'][4]['entries'][2]['option']['options']:
            if i['text'].replace('\n', '') == cluster_name:
                cluster_name = i['text']
                cluster_id = i['id']
                break

        # Let's build up the cluster mods
        cluster_mods = cluster.find_all("tr")

        cluster_prefixes = []
        cluster_suffixes = []
        for cluster_mod in cluster_mods[1:]:
            if "Added Small Passive Skills also grant" in cluster_mod.get_text():
                continue

            cluster_mod_info = remove_non_capital_prefixes(cluster_mod.get_text(separator=';'))

            cluster_mod_name = cluster_mod_info[0]
            cluster_mod_weight = cluster_mod_info[1]
            cluster_mod_level_req = cluster_mod_info[2]
            cluster_mod_type = cluster_mod_info[3]

            for entry in all_stats['result'][1]['entries']:
                if ("1 Added Passive Skill is " + cluster_mod_name) == entry['text']:
                    cluster_mod_id = entry['id']
                    break

            notable_info = {
                    'notableId': cluster_mod_id,
                    'notableName': cluster_mod_name,
                    # 'notableWeight': int(notableWeight),
                    # 'notableLevel': notableLevel,
                    # 'notableType': cluster_mod_type
                }

            if cluster_mod_type == "Prefix":
                cluster_prefixes.append(notable_info)
            else:
                cluster_suffixes.append(notable_info)

        comb_count = 0

        if cluster_size == "Large":
            comb_count = (len(cluster_prefixes) * (len(cluster_prefixes) - 1) * len(cluster_suffixes)) / 2
        elif cluster_size == "Medium":
            comb_count = (len(cluster_prefixes) * (len(cluster_prefixes) - 1)) / 2
        else:
            comb_count = len(cluster_prefixes)

        cluster_info = {
            'clusterId': cluster_id,
            'clusterName': cluster_name,
            'clusterCombCount': int(comb_count),
            'clusterPrefixCount': len(cluster_prefixes),
            'clusterSuffixCount': len(cluster_suffixes),
            'clusterPrefixes': cluster_prefixes,
            'clusterSuffixes': cluster_suffixes,
            # 'clusterNotables': listOfNotables,
            # 'clusterNotableCount': notableCount,
            # 'clusterNotableCombinationCount': combCount,
            # 'clusterNotableLevels': dict(sorted(notableLevelBreakpoint.items()))
        }

        list_of_clusters.append(cluster_info)

    print(f"{res.BgColors.BOLD}{res.BgColors.GREEN}Finished{res.BgColors.ENDC} fetching {res.BgColors.BOLD}{res.BgColors.BLUE}{cluster_size}{res.BgColors.ENDC} Cluster data!")

    return list_of_clusters

def update_cluster_data():

    leagues = requests.get('http://api.pathofexile.com/leagues', headers=headers)
    leagues = leagues.json()
    current_league = leagues[4]['id']  # current challenge league
    file_dir = "data"
    if (os.path.exists(file_dir) == False):
        os.mkdir(file_dir)
    if (os.path.exists(file_dir + "/clustermods") == False):
        os.mkdir(file_dir + "/clustermods")

    with open(file_dir + '/clustermods/small.json', 'w') as outfile:
        json.dump(get_poedb_data("Small"), outfile, indent=2)

    with open(file_dir + '/clustermods/medium.json', 'w') as outfile:
        json.dump(get_poedb_data("Medium"), outfile, indent=2)

    with open(file_dir + '/clustermods/large.json', 'w') as outfile:
        json.dump(get_poedb_data("Large"), outfile, indent=2)

update_cluster_data()