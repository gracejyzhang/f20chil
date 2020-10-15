import matplotlib.pyplot as plt


def plot_df(df, title, size):
    df.plot(kind='bar', stacked=False, width=1, logy=True, figsize=size, legend=False)
    plt.title(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 8})
    plt.tight_layout()
    plt.tick_params(axis='both', labelsize=8)
    plt.show()


def plot_3d(data, title, x_axis, y_axis, z_axis, size):
    fig = plt.figure(figsize=size)
    ax = fig.gca(projection='3d')
    index = 0
    shapes = ['o', 'v', 's', 'x', '*', 'D', 'P', '^', '1', 'p', '+', 'X', '<', '>']
    colours = ['b', 'g', 'r', 'c', 'y', 'k', 'm', 'tab:brown']
    for name, row in data.iterrows():
        ax.scatter(row[x_axis], row[y_axis], row[z_axis], label=name, c=colours[index % len(colours)], marker=shapes[index // len(colours)])
        index += 1
    ax.set_xlabel(x_axis, fontsize=8)
    ax.set_ylabel(y_axis, fontsize=8)
    ax.set_zlabel(z_axis, fontsize=8)
    ax.tick_params(axis='both', labelsize=8)
    fig.suptitle(title)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 8}, ncol=2)
    plt.tight_layout()
    plt.show()
