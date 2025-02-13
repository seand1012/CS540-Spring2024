import numpy as np
import scipy
import csv

def main():
    data = load_data('countries.csv')
    features = []
    # for i in range(2):
    #     features.append(calc_features(data[i]))
    features = calc_features(data[0])
    hac(features)
    

def load_data(filepath):
    data = []
    with open(filepath, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(dict(row))
    return data
            

def calc_features(row):
    vals = list(row.values())
    vals.remove(vals[0])
    vals.remove(vals[0])
    for element in vals:
        if(type(element) is not float):
            float(element)
    x = np.array(vals, dtype=np.float64)
    return x

def euc_dist(x,y):
    return np.linalg.norm(x - y)

def hac(features):
    n = len(features)
    distances = np.zeros((n,n)) # distance matrix, filled with zeros to start
    
    # populate distance matrix
    for i in range(n):
        for j in range(n):
            distances[i,j] = euc_dist(features[i], features[j])
            distances[j,i] = distances[i,j]
    
    cluster_nums = np.arange(n)
    z = []
    
    for k in range(n-1):
        min_dist = np.inf
        
        # find the next 2 closest pairs and assigns them to i and j
        i,j = np.unravel_index(np.argmin(distances), distances.shape)
        i_new,j_new = i,j
        # keep i < j for consistency
        if i > j:
            i, j = j, i
        
        # tiebreaking scenario
        for l in range(n):
            if l != i and l != j:
                new_dist = max(distances[i,l], distances[j,l])
                if new_dist < min_dist:
                    i_new, j_new = min(i,l), min(i, l)
                    min_dist = new_dist
                elif new_dist == min_dist:
                    if i < i_new:
                        i_new, j_new = i, j
                    elif i == i_new and l < j_new:
                        i_new, j_new = i, l
                    elif i == i_new and l == j_new and j < i_new:
                        i_new, j_new = i, j
                    
        # replace all nums = to j with i, leave all nums != to j alone
        # if cluster_nums == j, use j, otherwise use i
        cluster_nums = np.where(cluster_nums == j_new.astype(np.float64), i_new.astype(np.float64), cluster_nums)
        # i,j == indices of the 2 clusters being merged
        # distances[i,j] == complete linkage distances between i and j
        # k == current size of cluster, plus 2 for the new clusters being added
        z.append([i_new, j_new, min_dist, k + 2])
        
        # populate the rest of the distance matrix with merged clusters
        for l in range(n):
            if l != i and l != j:
                distances[i_new,l] = max(distances[i_new,l], distances[j_new,l])
                distances[l,i_new] = distances[i_new,l]
        
        # set distances for merged clusters to infinity
        distances[j_new,:] = np.inf
        distances[:,j_new] = np.inf
    print(np.array(z))
    return np.array(z)

def fig_hac(Z,names):
    pass

def normalize_features(features):
    pass




if __name__ == "__main__":
    main()