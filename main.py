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
    num_iterations = 100
    index_hub = 1300
    consts =   [      .005,            .005,            .005,           .3,                  .4999,                    .1,            .2,           .2,                 .0001] 
    # consts = c_gossip_stoppage, c_person_stoppage, c_friendship, c_juicy_change, c_transmission_probability, c_social_connection, c_juicy, c_speed_of_spread, c_number_of_times_heard

    ## c_gossip_stoppage            -> колико има утицаја коефицијент трача на његово заустављање
    ## c_person_stoppage            -> колико има утицаја коефицијент човека на заустављање трача
    ## c_friendship                 -> колико пријатељство има утицаја на заустављање трача
    ## c_juicy_change               -> колика је шанса да се сочност трача промени
    ## c_transmission_probability   -> колико уобичајена интерација има утицај на пренос трача
    ## c_social_connection          -> колико пријатељство има утицај на пренос трача
    ## c_juicy                      -> колико сочност трача има утицај на његов пренос
    ## c_speed_of_spread            -> колико брзина преноса има утицај на ширење трача
    ## c_number_of_times_heard      -> колико утицаја има поновно слушање трача на његово ширење

    file_path = "graphs/soc-sign-bitcoinotc.csv"
    G = MakeGraph(file_path, (-10, 10), (0, 1))

    # Прављење мреже
    people = []
    num_people = G.number_of_nodes()
    for i in G.nodes():
        gossip_modifier_constant = random.random() * 2 - 1
        gossip_stoppage_constant = random.random()
        speed_of_spread = random.random()
        people.append(Person(i, gossip_modifier_constant, gossip_stoppage_constant, speed_of_spread))
    people_dict = {person.id: person for person in people}

    # Учитавање хабова
    hubs = []
    with open('hubs.txt', 'r') as file:
        for line in file.readlines():
            node, degree = map(int, line.split(','))
            hubs.append((node, degree))

    # Прављење трача
    gossip_id_counter = 0
    person_gossiped_about_id = hubs[index_hub][0]
    gossip_juicy = random.random()
    gossip_stoppable = random.random()
    main_gossip = Gossip(gossip_id_counter, person_gossiped_about_id, gossip_juicy, gossip_stoppable)
    gossip_id_counter += 1

    # Листа за чување резултата свих итерација
    all_infected_counts = []
    all_paths_infected = []
    
    # Име фајла у којем се чувају подаци
    file_name = f'gossip_about_hub_index_{index_hub}_it_{num_iterations}'
    
    # Покретање симулација
    for i in tqdm(range(num_iterations)):
        max_infected_count, infected_count_over_time, path_infected = RunSingleSimulation(
            G, people_dict, transmission_probability, simulation_days, main_gossip
        )
        all_infected_counts.append(infected_count_over_time)
        all_paths_infected.append(path_infected)

    # Израчунавање просека резултата
    average_infected_counts = np.mean(all_infected_counts, axis = 0)
    average_infected_percentage = average_infected_counts / max_infected_count * 100

    # Испис метрика на крају симулације (са просечним вредностима)
    max_infected_percentage = (max_infected_count / num_people) * 100               # максимални обим ширења
    total_infected_percentage = (average_infected_counts[-1] / num_people) * 100    # остварени обим ширења у целој популацији
    total_possible_infected_percentage = average_infected_percentage[-1]            # остварени обим ширења у популацији која може да сазна
    time_to_50_percent = -1                                                         # време до 50% максималног обима заразе 
    for day, count in enumerate(average_infected_percentage):
        if time_to_50_percent == -1 and count >= 50:
            time_to_50_percent = day
    time_to_90_percent = -1                                                         # време до 50% максималног обима заразе 
    for day, count in enumerate(average_infected_percentage):
        if time_to_90_percent == -1 and count >= 90:
            time_to_90_percent = day

    with open(f'results/{file_name}.txt', '+w') as file:
        file.write(f"Проценат популације који може да сазна трач: {max_infected_percentage:.2f}% популације може да сазна трач\n")
        file.write(f"Просек ширења трача у целој популацији: {total_infected_percentage:.2f}% популације је сазнало трач.\n")
        file.write(f"Просек ширења трача у популацији која може да сазна: {total_possible_infected_percentage:.2f}% популације је сазнало трач.\n")
        if time_to_50_percent != -1:
            file.write(f"Просечно време док трач не дође до 50% могућих људи: {time_to_50_percent} дана.\n")
        else:
            file.write("Трач није достигао 50% могућих људи у току симулација.\n")
        if time_to_90_percent != -1:
            file.write(f"Просечно време док трач не дође до 90% могућих људи: {time_to_90_percent} дана.\n")
        else:
            file.write("Трач није достигао 90% могућих људи у току симулација.\n")

    # Путања ширења трача
    with open(f'raw_data/num_infected/{file_name}.txt', '+w') as file:
        file.writelines([str(result) + '\n' for result in all_infected_counts])
    with open(f'raw_data/paths/{file_name}.txt', '+w') as file:
        file.writelines([str(path) + '\n' for path in all_paths_infected])
    with open(f'raw_data/consts/{file_name}.txt', '+w') as file:
        file.write(str(consts))

    # Приказ криве ширења
    plt.figure(figsize=(10, 6))
    plt.plot(average_infected_percentage, marker='o', linestyle='-', color='blue')
    plt.title('Просечно ширење трача кроз време')
    plt.xlabel('Дан симулације')
    plt.ylabel('Просечан проценат могућих особа које знају трач')
    plt.grid(True)
    plt.savefig(f'figs/{file_name}.jpg')

if __name__ == '__main__':
    main()