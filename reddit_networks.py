import networkx as nx
import json
import os

def process(file):
    graph = nx.DiGraph()
    with open(file) as fp:
        months = json.load(fp)
    for month in months:
        for user in month:
            graph.add_node(user)
            for association in month[user]:
                # adds edge from the user who replied to the user who was replied to
                graph.add_edge(user, association)
    return graph

if __name__ == '__main__':
    directory = 'datasets/reddit_politics'
    for file in os.listdir(directory):
        filename = 'results/reddit_networks/' + file.replace('.json', '') + '.txt'
        if not os.path.isfile(filename):
            open(filename, 'w').close()
        nx.write_adjlist(process(os.path.join(directory, file)), filename)
