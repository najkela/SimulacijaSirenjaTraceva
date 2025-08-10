import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Формирање графа за анализу
    file_path = "graphs/facebook_combined.txt"
    G = nx.read_edgelist(file_path, nodetype=int, create_using=nx.Graph())


    # Основне карактеристике мреже
    print("\n--- Основне карактеристике ---")
    print(f"Број чворова (N): {G.number_of_nodes()}")
    print(f"Број ивица (E): {G.number_of_edges()}")
    density = nx.density(G)
    print(f"Густина мреже: {density:.4f}")
    num_components = nx.number_connected_components(G)
    print(f"Број повезаних компоненти: {num_components}")


    # Карактеристике веза и кластера
    print("\n--- Карактеристике веза и кластера ---")

    ## Просечан степен и дистрибуција степена
    avg_node_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
    print(f"Просечан степен: {avg_node_degree:.2f}")
    degree_counts = dict(G.degree()).values()
    plt.hist(degree_counts, bins=1000)
    plt.show()

    ## Просечан коефицијент класеровања и дистрибуција коефицијента кластеровања
    avg_clustering_coefficient = nx.average_clustering(G)
    print(f"Просечан коефицијент кластеризације: {avg_clustering_coefficient:.4f}")
    clustering_counts = list(nx.clustering(G).values())
    plt.hist(clustering_counts, bins=1000)
    plt.show()

    ## Коефицијент асортативности степенова - колика је зависност чворова истог степена да буду повезани [-1, 1]
    assortativity_coefficient = nx.degree_assortativity_coefficient(G)
    print(f"Коефицијент асортативности (степен): {assortativity_coefficient:.4f}")


    # Централност и утицај чворова
    print("\n--- Централност и утицај чворова ---")

    ## Централност степена - колико процената чворова су њему суседи
    degree_centrality = nx.degree_centrality(G)
    degree_centrality_counts = list(degree_centrality.values())
    plt.hist(degree_centrality_counts, bins=1000)
    plt.show()

    ## Централност блискости
    closeness_centrality = nx.closeness_centrality(G)
    closeness_centrality_counts = list(closeness_centrality.values())
    plt.hist(closeness_centrality_counts, bins=1000)
    plt.show()

    ## Централност посредништва (може бити спора за велике графове, размислите о k параметру за апроксимацију)
    betweenness_centrality = nx.betweenness_centrality(G, k=1000) # k=1000 за апроксимацију
    betweenness_centrality_counts = list(betweenness_centrality.values())
    plt.hist(betweenness_centrality_counts, bins=1000)
    plt.show()

    ## Асиметрија централности
    asymmetry_degree = np.std(degree_centrality_counts) / np.mean(degree_centrality_counts)
    print(f"Асиметрија централности степена (коефицијент варијације): {asymmetry_degree:.4f}")

    # Визуелизација
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
    plt.show()

if __name__ == '__main__':
    main()