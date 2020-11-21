import networkx as nx
import json
import os
import pandas as pd
import sys


dir = 'datasets/reddit_politics'
triads_out = 'results/reddit_politics_sd/reddit.csv'
info_out = 'results/reddit_politics_sd/reddit_info.csv'
users_out = 'results/reddit_politics_sd/reddit_users.csv'

try:
    skip = set(map(lambda s: s.strip(), open('skip.txt').readlines()))
except:
    skip = set()


def process_subreddit(file, triads, info, names, users):
    with open(os.path.join(dir, file)) as fp:
        months = json.load(fp)
    for i in range(len(months)):
        try:
            graph = nx.DiGraph()
            for user in months[i]:
                graph.add_node(user)
                for association in months[i][user]:
                    # adds edge from the user who replied to the user who was replied to
                    graph.add_edge(user, association)
            names.append(file.replace('.json', '') + ' ' + str(i))
            triads.append(nx.triadic_census(graph))
            info.append({'nodes': nx.number_of_nodes(graph), 'edges': nx.number_of_edges(graph)})
            users.update(graph.nodes)
        except:
            continue


# process each file in a directory as independent graphs
def process_dir():
    for file in os.listdir(dir):
        if file in skip:
          continue
        triads, info, names, users = [], [], [], set()
        process_subreddit(file, triads, info, names, users)
        triads_df = pd.DataFrame(triads, index=names)
        info_df = pd.DataFrame(info, index=names)
        triads_df.to_csv(triads_out, mode='a', header=False)
        info_df.to_csv(info_out, mode='a', header=False)
        # process_users(file, users)
        print(file)
        sys.stdout.flush()


def process_users(file, users):
    if not os.path.isfile(users_out):
        with open(users_out, mode='w') as out_json:
            entry = {file.replace('.json', ''): list(users)}
            json.dump(entry, out_json)
    else:
        with open(users_out, mode='r', encoding ='utf-8') as in_json:
            users_json = json.load(in_json)
        with open(users_out, mode='w', encoding='utf-8') as out_json:
            users_json[file.replace('.json', '')] = list(users)
            json.dump(users_json, out_json)


if __name__ == '__main__':
    process_dir()




