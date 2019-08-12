import numpy as np

#  find the paths with minimum cost (shortest path) in a graph, from a source node s to several nodes (d)
#  the graph is known through an adjacency matrix, where adj(i,j)=cost for going from i to j; exception if adj(i,j)==0 - see below
#  Dijkstra's algorithm is used (since it finds minimal costs for all nodes in graph), with the following small modification:
#  if adj(i,j)==0, (i~=j), then there is no transition from i to j, so this 0 is not a cost
#  (this is done because we want that adj be a sparse matrix, for managing more states;
#  we will check to not have costs less than precision, which could be approximated with 0)
#  s - index for soure node (scalar), d - row vector with indices for destination nodes
#  path will be a cell array, path{i} will be a vector giving the path s -> d(i)

def findMatches(a,b,c,d):
    # a value and b matrix and c value and d matrix
    ret = []
    counter = 0
    for x,y in zip(b,d):
        if x == a and y == c:
            ret.append(counter)
            break
        counter = counter + 1
    return ret

def findMatchesForNotZero(a,b,c,d):
    # a value and b matrix and c value and d matrix
    ret = []
    counter = 0
    for x,y in zip(b,d):
        if x != a and y == c:
            ret.append(counter)
            break
        counter = counter + 1
    return ret

def indiceswhere0Elements(n):
    #n is a 1 X n  matrix
    ret = []
    for counter,i in enumerate(n):
        if i == 0:
            ret.append(counter)
    return ret

# def findMin(array):
#     #given an array find the min element in it





def FindPaths(adj,s,d):

    d = [item for sublist in d for item in sublist]  # convert d appropriate list
    n = np.shape(adj)[0]  # no. of nodes
    visited = np.zeros((1,n))  # if a node was considered, it has a value 1 in vector "visited"
    dist = np.ones((1,n)) * np.inf  # disatnces from the s node (will be modifies)
    dist = [item for sublist in dist for item in sublist]
    dist[s[0]] = 0
    predec = np.zeros((1,n))  # predecessor to each node

    #  search until all nodes are visited
    while np.sum(visited) != n:
        # tmp_visites_index = np.where(visited == 0)[0]
        tmp_zero_indices =  indiceswhere0Elements(visited[0])
        # d_m = int(np.min(dist[0:np.shape(tmp_visites_index)[0]]))  # min distance from source, considering only unvisited states
        new_dist = []
        for i in tmp_zero_indices:
            new_dist.append(dist[i])
        d_m = np.min(new_dist)
        # x = np.where(np.any(dist == d_m and visited == 0))
        x = findMatches(d_m,dist,0,visited[0,:])
        # if len(x) == 0:
        #     continue
        x = x[0]  # if there are mode nodes at the same distance, they will be considered at the following iteration
        visited[0][x] = 1
        # neigh = np.where(adj[x,:] != 0 and visited == 0)
        neigh = findMatchesForNotZero(0,adj[x,:],0,visited[0,:])
        if len(neigh) == 0:
            continue
        for i in neigh:
            if dist[i] > dist[x] + adj[x,i]:
                dist[i] = dist[x] + adj[x,i]
                predec[0][i] = x

    paths = []
    for i in range(len(d)):
        if (dist[d[i]]) != np.Inf:
            path = [d[i]]
            while path[0] != s:
                path.append(predec[path[0]])
        else:
            path = []
        paths.insert(i,path)
    return paths
