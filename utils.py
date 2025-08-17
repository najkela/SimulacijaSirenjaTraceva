import networkx as nx
import random
from classes import Gossip

# Прави граф на основу фајла који му се додели
def MakeGraph(file_path : str, input_range : tuple[int, int] = None, output_range : tuple[int, int] = None) -> nx.Graph:
    extension = file_path.split('.')[-1]
    if extension == 'txt': return nx.read_edgelist(file_path, nodetype=int, create_using=nx.Graph())
    elif extension == 'csv':
        G = nx.Graph()
        with open(file_path) as file:
            for line in file:
                args = line.split(',')
                weight = (float(args[2]) - input_range[0]) * (output_range[1] - output_range[0]) / (input_range[1] - input_range[0]) + output_range[0]
                G.add_edge(int(args[0]), int(args[1]), weight = weight)
        return G

# Функција која покреће једну симулацију и враћа резултате
def RunSingleSimulation(
        G : nx.graph, 
        people_dict : dict, 
        transmission_probability : float, 
        simulation_days : int,
        gossip : Gossip = None):
    
    # Прављење трача ако није исти за сваку симулацију
    if gossip == None:
        gossip_id_counter = 0
        person_gossiped_about_id = random.choice(list(people_dict.keys()))
        gossip = Gossip(gossip_id_counter, person_gossiped_about_id)
    
    # Ресетовање стања свих особа на почетак симулације
    for person in people_dict.values():
        person.state = 'Susceptible'
        person.known_gossips = {}

    # Бирање и постављање почетно заражене особе
    acquaintances_of_gossip_target = list(G.neighbors(gossip.person_gossiped_about_id))
    num_initial_infected = 1
    initial_infected_ids = random.sample(acquaintances_of_gossip_target, num_initial_infected)

    for person_id in initial_infected_ids:
        people_dict[person_id].state = 'Infected'
        people_dict[person_id].known_gossips[gossip.id] = gossip.person_gossiped_about_id

    # Чување параметара ширења кроз време
    infected_count_over_time = [num_initial_infected]

    # Рачунање популације која може да сазна трач и њихово пребројавање
    people_can_know_gossip = acquaintances_of_gossip_target.copy()
    people_can_know_gossip += [new_id for person_id in acquaintances_of_gossip_target for new_id in list(G.neighbors(person_id))]
    people_can_know_gossip = list(set(people_can_know_gossip))
    people_can_know_gossip.remove(gossip.person_gossiped_about_id)
    max_infected_count = len(people_can_know_gossip)

    # Симулација
    for day in range(simulation_days):
        # Провера да ли постоји још неко ко може да сазна трач
        if infected_count_over_time[-1] == max_infected_count: 
            infected_count_over_time.append(max_infected_count)
            continue
        
        # Зараза ако постоји неко ко може да се зарази
        newly_infected_ids = []

        for person_id, current_person in people_dict.items():
            # Могуће ширење заразе ако је тренутна особа заражена
            if current_person.state == 'Infected':
                # Особе које могу бити заражене
                neighbors = list(G.neighbors(person_id))
                for neighbor_id in neighbors:
                    neighbor_person = people_dict[neighbor_id]
                    # Да ли ће се тренутна особа заразити
                    if neighbor_person.state == 'Susceptible' and random.random() < ChanceForInfection_0(transmission_probability, neighbor_id, people_can_know_gossip):
                        newly_infected_ids.append(neighbor_id)
                        neighbor_person.known_gossips[gossip.id] = gossip.person_gossiped_about_id
        
        for person_id in newly_infected_ids:
            people_dict[person_id].state = 'Infected'
        
        current_infected_count = sum(1 for person in people_dict.values() if person.state == 'Infected')
        infected_count_over_time.append(current_infected_count)
    
    return max_infected_count, infected_count_over_time

def ChanceForInfection_0(transmission_probability, neighbor_id, people_can_know_gossip): return transmission_probability if neighbor_id in people_can_know_gossip else 0