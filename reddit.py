import networkx as nx
import json
import os
import pandas as pd


def grow(file, graph):
    with open(file) as fp:
        months = json.load(fp)
    for month in months:
        for user in month:
            graph.add_node(user)
            for association in month[user]:
                # adds edge from the user who replied to the user who was replied to
                graph.add_edge(user, association)


# process each file in a directory as independent graphs
def process_dir(directory):
    subs = []
    triads = []
    info = []
    for filename in os.listdir(directory):
        print(filename)
        graph = nx.DiGraph()
        grow(os.path.join(directory, filename), graph)
        subs.append(filename.replace('.json', ''))
        triads.append(nx.triadic_census(graph))
        info.append({'nodes':nx.number_of_nodes(graph), 'edges':nx.number_of_edges(graph)})
    triads_df = pd.DataFrame(triads, index=subs)
    info_df = pd.DataFrame(info, index=subs)
    return triads_df, info_df


# process all files as one graph
def process_exp(files):
    graph = nx.DiGraph()
    for file in files:
        grow(file, graph)
    triads_df = pd.DataFrame([nx.triadic_census(graph)], index=[' + '.join(files)])
    info_df = pd.DataFrame([{'nodes': nx.number_of_nodes(graph), 'edges': nx.number_of_edges(graph)}],
                           index=[' + '.join(files)])
    return triads_df, info_df


# process each file in a directory as independent graphs
def process_append(directory, triads_file, info_file):
    for filename in os.listdir(directory):
        print(filename)
        graph = nx.DiGraph()
        grow(os.path.join(directory, filename), graph)
        name = filename.replace('.json','')
        triads_df = pd.DataFrame([nx.triadic_census(graph)], index=[name])
        info_df = pd.DataFrame([{'nodes':nx.number_of_nodes(graph), 'edges':nx.number_of_edges(graph)}], index=[name])
        triads_df.to_csv(triads_file, mode='a', header=False)
        info_df.to_csv(info_file, mode='a', header=False)


if __name__ == '__main__':
    process_append('datasets/reddit', 'results/reddit_reply.csv', 'results/reddit_reply_info.csv')
