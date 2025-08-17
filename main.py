import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from classes import Person, Gossip
from utils import *
from tqdm import tqdm

def main():
    # Параметри за симулацију
    transmission_probability = 0.02
    simulation_days = 25
    num_iterations = 50

    file_path = "graphs/soc-sign-bitcoinotc.csv"
    G = MakeGraph(file_path, (-10, 10), (0, 1))

    # Прављење мреже
    people = []
    num_people = G.number_of_nodes()
    for i in G.nodes():
        gossip_modifier_constant = random.random() * 2 - 1
        people.append(Person(i, gossip_modifier_constant))
    people_dict = {person.id: person for person in people}

    # Прављење трача
    gossip_id_counter = 0
    person_gossiped_about_id = random.choice(list(people_dict.keys()))
    gossip_juicy = random.random()
    main_gossip = Gossip(gossip_id_counter, person_gossiped_about_id, gossip_juicy)
    gossip_id_counter += 1

    # Листа за чување резултата свих итерација
    all_infected_counts = []
    
    # Покретање симулација
    print(f"Покретање {num_iterations} симулација...")
    for i in tqdm(range(num_iterations)):
        max_infected_count, infected_count_over_time = RunSingleSimulation(
            G, people_dict, transmission_probability, simulation_days, main_gossip
        )
        all_infected_counts.append(infected_count_over_time)

    # Израчунавање просека резултата
    average_infected_counts = np.mean(all_infected_counts, axis = 0)
    average_infected_percentage = average_infected_counts / max_infected_count * 100

    # Испис метрика на крају симулације (са просечним вредностима)
    print("\n--- Просечни резултати из свих симулација ---")

    ## максимални обим ширења
    max_infected_percentage = (max_infected_count / num_people) * 100
    print(f"Проценат популације који може да сазна трач: {max_infected_percentage:.2f}% популације може да сазна трач")

    ## остварени обим ширења у целој популацији
    total_infected_percentage = (average_infected_counts[-1] / num_people) * 100
    print(f"Просек ширења трача у целој популацији: {total_infected_percentage:.2f}% популације је сазнало трач.")

    ## остварени обим ширења у популацији која може да сазна
    total_possible_infected_percentage = average_infected_percentage[-1]
    print(f"Просек ширења трача у популацији која може да сазна: {total_possible_infected_percentage:.2f}% популације је сазнало трач.")

    ## време до 50% максималног обима заразе 
    time_to_50_percent = -1
    for day, count in enumerate(average_infected_percentage):
        if time_to_50_percent == -1 and count >= 50:
            time_to_50_percent = day
    if time_to_50_percent != -1:
        print(f"Просечно време док трач не дође до 50% могућих људи: {time_to_50_percent} дана.")
    else:
        print("Трач није достигао 50% могућих људи у току симулација.")
    
    ## време до 90% максималног обима заразе 
    time_to_90_percent = -1
    for day, count in enumerate(average_infected_percentage):
        if time_to_90_percent == -1 and count >= 90:
            time_to_90_percent = day
    if time_to_90_percent != -1:
        print(f"Просечно време док трач не дође до 90% могућих људи: {time_to_90_percent} дана.")
    else:
        print("Трач није достигао 90% могућих људи у току симулација.")

    ## приказ криве ширења
    plt.figure(figsize=(10, 6))
    plt.plot(average_infected_percentage, marker='o', linestyle='-', color='blue')
    plt.title('Просечно ширење трача кроз време')
    plt.xlabel('Дан симулације')
    plt.ylabel('Просечан проценат могућих особа које знају трач')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()