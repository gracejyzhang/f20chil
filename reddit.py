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


# process all files matching each expression as one graph
def process_exp(expressions):
    exp = []
    triads = []
    info = []
    for expression in expressions:
        print(expression)
        exp.append(expression) # clean up expression
        graph = nx.DiGraph()
        for file in glob.glob(expression):
            grow(file, graph)
        triads.append(nx.triadic_census(graph))
        info.append({'nodes':nx.number_of_nodes(graph), 'edges':nx.number_of_edges(graph)})
    triads_df = pd.DataFrame(triads, index=exp)
    info_df = pd.DataFrame(info, index=exp)
    return triads_df, info_df


if __name__ == '__main__':
    triads_df, info_df = process_exp(['reddit_reply/*'])
    triads_df.to_csv('results/reddit_reply_overall_triads.csv')
    info_df.to_csv('results/reddit_reply_overall_info.csv')


