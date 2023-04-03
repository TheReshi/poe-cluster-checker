import get_cluster_data as gcd
import resources as res
import price_check as pc
import combinations as comb

if __name__ == "__main__":
    gcd.update_cluster_data()
    comb.update_comb_data()
    pc.check_prices()