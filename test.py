import price_check as pc
import resources as res
import count_combs as cc
import json, time
import get_cluster_data as gcd
import combinations as combs
import os

# with open("data/clustercombs/large.json", 'r') as infile:
#     cluster_data = json.load(infile)

# comb_count = cc.count_combs('Large')
# current_comb = 0

# for cluster in cluster_data:
#     cluster_id = int(cluster["clusterId"])
#     cluster_name = cluster["clusterName"].replace("\n", "")
#     cluster_combs = int(cluster["clusterCombCount"])

#     for combs in cluster["clusterCombs"]:
#         current_comb += 1

#         item_price = pc.get_item_prices(cluster_id, combs)
#         print(f'[{res.BgColors.BLUE}{comb_count} / {current_comb}{res.BgColors.ENDC}][{res.BgColors.GREEN}{cluster_combs} / {current_comb}{res.BgColors.ENDC}] {cluster_id} {cluster_name} | {", ".join([comb["notableName"] for comb in combs])}: {item_price}')

#         writeable_price = [str(i) for i in item_price]
        
#         if len(item_price) > 0:
#             res.debug(f'{cluster_id};{cluster_name};{combs[0]["notableName"]};{combs[1]["notableName"]};{combs[2]["notableName"]};{";".join(writeable_price)}')
#             with open("data/output/prices.csv", 'a+') as outfile:
#                 outfile.write(f'{cluster_id};{cluster_name};{combs[0]["notableName"]};{combs[1]["notableName"]};{combs[2]["notableName"]};{";".join(writeable_price)}\n')

#         time.sleep(5)

def pricecheck_cluster(cluster_size):
    with open(f"data/clustercombs/{cluster_size.lower()}.json", 'r') as infile:
        cluster_data = json.load(infile)

    if os.path.exists(f"data/output/{cluster_size.lower()}_prices.csv"):
        with open(f"data/output/{cluster_size.lower()}_prices.csv", "w") as file:
            if cluster_size.lower() == "large":
                file.write("Cluster ID;Cluster Name;Prefix 1;Prefix 2;Suffix;Price 1;Price 2;Price 3;Price 4;Price 5\n")
            else:
                file.write("Cluster ID;Cluster Name;Prefix 1;Prefix 2;Price 1;Price 2;Price 3;Price 4;Price 5\n")

    comb_count = cc.count_combs(cluster_size)
    current_comb = 0

    for cluster in cluster_data:
        cluster_id = int(cluster["clusterId"])
        cluster_name = cluster["clusterName"].replace("\n", "")
        cluster_combs = int(cluster["clusterCombCount"])
        current_comb_local = 0

        for combs in cluster["clusterCombs"]:
            current_comb += 1
            current_comb_local += 1

            item_price = pc.get_item_prices(cluster_id, combs)

            if len(item_price) > 5:
                item_price = item_price[:5]

            print(f'[{res.BgColors.OKBLUE}{comb_count} / {current_comb}{res.BgColors.ENDC}][{res.BgColors.GREEN}{cluster_combs} / {current_comb_local}{res.BgColors.ENDC}] {cluster_id} {cluster_name} | {", ".join([comb["notableName"] for comb in combs])}: {item_price}')

            writable_price = [str(i) for i in item_price]
            
            if len(item_price) > 0:
                res.debug(f'{cluster_id};{cluster_name};{";".join([comb["notableName"] for comb in combs])};{";".join(writable_price)}')
                with open(f"data/output/{cluster_size.lower()}_prices.csv", 'a+') as outfile:
                    outfile.write(f'{cluster_id};{cluster_name};{";".join([comb["notableName"] for comb in combs])};{";".join(writable_price)}\n')

            time.sleep(5)

combs.update_comb_data()
pricecheck_cluster("Medium")
pricecheck_cluster("Large")
print(pc.non_added)