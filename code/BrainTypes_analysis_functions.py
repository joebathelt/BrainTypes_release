from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Unicode']
rcParams['text.usetex'] = True
rcParams['axes.labelsize'] = 9
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9
mm2inches = 0.039371
single_column = 90*mm2inches
double_column = 190*mm2inches
one_half_column = 140*mm2inches

def get_imaging_ID(ID_string, ID_table):
    """
    #================================
    # Helper function to match CALM behavioural and imaging IDs
    #================================

    inputs:
    ID_string: string with the behavioural ID
    ID_table: filename of the csv file that matches behavioural and imaging IDs

    outputs:
    ID: imaging ID matching the behavioural ID
    """

    # Reading data from the lookup table
    import pandas as pd
    data = pd.Series.from_csv(ID_table)

    # Removing brackts
    import re
    for counter in range(1,len(data)):
        entry = data[counter]
        if re.search(r"[(){}[\]]+",str(entry)):
            data[counter] = entry[1:-1]

    # Getting the matching ID
    try:
        ID = data[data.index == ID_string].values.tolist()
        return ID[0]
    except:
        return float('nan')


def get_consensus_module_assignment(network, iterations):
    """
    #================================
    # Obtain the consensus module structure
    #================================

    inputs:
    adjacency_matrix: adjacency_matrix
    gamma: gamma value

    outputs:
    vector of module assignment for each node
    """


    import numpy as np
    consensus_matrices = list()

    for i in range(0,iterations):
        consensus_matrix,modules,q = get_consensus_matrix(network)
        consensus_matrices.append(consensus_matrix)

    mean_consensus_matrix = np.mean(consensus_matrices,axis=0)

    consensus_matrix,modules,q = get_consensus_matrix(mean_consensus_matrix)
    consensus_matrix2,modules,q = get_consensus_matrix(mean_consensus_matrix)

    while abs(np.sum(consensus_matrix - consensus_matrix2)) != 0:
        consensus_matrix,modules,q = get_consensus_matrix(mean_consensus_matrix)
        consensus_matrix2,modules,q = get_consensus_matrix(mean_consensus_matrix)

    return (modules, q)

def get_consensus_matrix(network):
    """
    #================================
    # Helper function for consensus module assignment
    #================================

    inputs:
    network: numpy array of an adjacency matrix
    """


    import bct
    import numpy as np
    modules,q = bct.modularity_louvain_und_sign(network, qtype='smp')
    module_matrix = np.repeat(modules,repeats=network.shape[0])
    module_matrix = np.reshape(module_matrix,newshape=network.shape)
    consensus_matrix = module_matrix == module_matrix.transpose()
    return (consensus_matrix.astype('float'), modules, q)

def plot_community_matrix(network, community_affiliation):
    """
    #================================
    # Plot an adjacency matrix with module assignment
    #================================

    inputs:
    network: numpy array of an adjacency matrix
    community_affiliation: array indicating which node belongs to which module/community
    """


    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    sorting_array = sorted(range(len(community_affiliation)), key=lambda k: community_affiliation[k])
    sorted_network = network[sorting_array, :]
    sorted_network = sorted_network[:, sorting_array]
    plt.figure(figsize=(one_half_column/2, one_half_column/2), dpi=300)
    im = plt.imshow(sorted_network,
               cmap='bwr',
               interpolation='none',
               vmin=-1, vmax=1)
    ax = plt.gca()
    ax.grid('off')
    ax.set_xticklabels(' ')
    ax.set_yticklabels(' ')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cb = plt.colorbar(im, cax=cax)
    cb.set_label('Pearson correlation coefficient R')
    cb.ax.yaxis.set_label_position('right')
    plt.tight_layout(pad=0, w_pad=1, h_pad=0)

def plot_spring_layout(results, communities, threshold):
    """
    #================================
    Plot community affiliation in a spring layout
    #================================

    inputs:
    results: pandas dataframe with cognitive variables
    communities: numpy array of community affiliation
    threshold: Pearson corrletion threshold
    """

    import bct
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    from scipy.stats import zscore

    results[results.columns] = results.apply(zscore)
    correlation_matrix = results.transpose().corr().values

    plt.figure(figsize=(one_half_column/2, one_half_column/2), dpi=300)
    G=nx.from_numpy_matrix(bct.threshold_absolute(correlation_matrix, threshold))
    colours = ['#FF8C00', '#FFD700', '#D3D3D3']

    pos=nx.spring_layout(G)

    for community in np.unique(communities):

        nx.draw_networkx_nodes(G,pos,
                               nodelist=np.where(communities == community)[0].tolist(),
                               node_color=colours[community-1],
                               node_size=40,
                               alpha=0.8)


    nx.draw_networkx_edges(G,pos,width=0.5,alpha=0.5)
    plt.axis('off');
    plt.legend(['C' + str(community) for community in np.unique(communities) ])
