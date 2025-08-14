import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from utils import *

def main():
    # Формирање графа за анализу
    file_path = "graphs/soc-sign-bitcoinotc.csv"
    G = MakeGraph(file_path, input_range = (-10, 10), output_range = (0, 1))
    _, ax = plt.subplots(nrows=2, ncols=3)

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
    ax[0, 0].set_title("Дистрибуција степена")
    ax[0, 0].hist(degree_counts, bins=1000)

    ## Просечан коефицијент класеровања и дистрибуција коефицијента кластеризације
    avg_clustering_coefficient = nx.average_clustering(G)
    print(f"Просечан коефицијент кластеризације: {avg_clustering_coefficient:.4f}")
    clustering_counts = list(nx.clustering(G).values())
    ax[0, 1].set_title("Дистрибуција коефицијената кластеризације")
    ax[0, 1].hist(clustering_counts, bins=1000)

    ## Коефицијент асортативности степенова - колика је зависност чворова истог степена да буду повезани [-1, 1]
    assortativity_coefficient = nx.degree_assortativity_coefficient(G)
    print(f"Коефицијент асортативности (степен): {assortativity_coefficient:.4f}")


    # Централност и утицај чворова
    print("\n--- Централност и утицај чворова ---")

    ## Централност степена - колико процената чворова су њему суседи
    degree_centrality = nx.degree_centrality(G)
    degree_centrality_counts = list(degree_centrality.values())
    ax[1, 0].set_title("Дистрибуција централности степена")
    ax[1, 0].hist(degree_centrality_counts, bins=1000)

    ## Централност блискости
    closeness_centrality = nx.closeness_centrality(G)
    closeness_centrality_counts = list(closeness_centrality.values())
    ax[1, 1].set_title("Дистрибуција централности блискости")
    ax[1, 1].hist(closeness_centrality_counts, bins=1000)

    ## Централност посредништва
    betweenness_centrality = nx.betweenness_centrality(G, k=1000) # k=1000 за апроксимацију
    betweenness_centrality_counts = list(betweenness_centrality.values())
    ax[1, 2].set_title("Дистрибуција централности посредништва")
    ax[1, 2].hist(betweenness_centrality_counts, bins=1000)

    ## Асиметрија централности
    asymmetry_degree = np.std(degree_centrality_counts) / np.mean(degree_centrality_counts)
    print(f"Асиметрија централности степена (коефицијент варијације): {asymmetry_degree:.4f}")

    # Приказ графика
    plt.show()

    # Визуелизација
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
    plt.show()

    return

if __name__ == '__main__':
    main()