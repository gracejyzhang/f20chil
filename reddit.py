import networkx as nx
import json
import os
import glob
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
    info_df = pd.DataFrame([{'nodes':nx.number_of_nodes(graph), 'edges':nx.number_of_edges(graph)}],
                           index=[' + '.join(files)])
    return triads_df, info_df


if __name__ == '__main__':
    triads_df, info_df = process_exp(['reddit_reply/socialism.json', 'reddit_reply/Libertarian.json'])
    triads_df.to_csv('results/socialism-libertarian.csv')
    info_df.to_csv('results/socialism-libertarian_info.csv')

    triads_df, info_df = process_exp(['reddit_reply/Republican.json', 'reddit_reply/Conservative.json', 'reddit_reply/conservatives.json'])
    triads_df.to_csv('results/conservative-republican.csv')
    info_df.to_csv('results/conservative-republican_info.csv')




