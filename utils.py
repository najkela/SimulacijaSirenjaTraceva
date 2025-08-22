import networkx as nx
import random
from classes import *

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
        gossip : Gossip = None) -> float:
    
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
        people_dict[person_id].known_gossips[gossip.id] = [person.id]

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
                current_path = current_person.known_gossips[gossip.id]
                # Особе које могу бити заражене
                neighbors = list(G.neighbors(person_id))
                for neighbor_id in neighbors:
                    neighbor_person = people_dict[neighbor_id]
                    # Да ли ће се тренутна особа заразити
                    if random.random() < ChanceForInfection(transmission_probability, G, current_person, neighbor_person, people_can_know_gossip, gossip):
                        newly_infected_ids.append(neighbor_id)
                        neighbor_person.known_gossips[gossip.id] = current_path + [neighbor_id]

                    # Број пута колико је особа чула трач се повећава сваки пут кад буде изложена информацији
                    neighbor_person.gossips_heard[gossip.id] = neighbor_person.gossips_heard.get(gossip.id, 0) + 1
        
        for person_id in newly_infected_ids:
            people_dict[person_id].state = 'Infected'
        
        current_infected_count = sum(1 for person in people_dict.values() if person.state == 'Infected')
        infected_count_over_time.append(current_infected_count)
    
    return max_infected_count, infected_count_over_time

def ChanceForInfection_0(transmission_probability : float, neighbor_person : Person, people_can_know_gossip : list[Person]) -> float: 
    return transmission_probability if neighbor_person.id in people_can_know_gossip and neighbor_person.state == 'Susceptible' else 0

def ChanceForInfection_1(transmission_probability : float, G : nx.Graph, current_person : Person, neighbor_person : Person, people_can_know_gossip : list[Person], gossip : Gossip) -> float:
    if not ChanceForInfection_0(transmission_probability, neighbor_person, people_can_know_gossip):
        return 0
    
    weight = G.edges[current_person.id, neighbor_person.id]['weight']
    try:
        friendship = G.edges[current_person.id, gossip.person_gossiped_about_id]['weight']
    except:
        friendship = 0

    # Константе за утицај коефицијената на шансу преноса
    c_transission, c_weight = .9, .1    # збир мора да буде 1

    return c_transission * transmission_probability + c_weight * (weight - friendship)

def ChanceForInfection_2(transmission_probability : float, neighbor_person : Person, people_can_know_gossip : list[Person], gossip : Gossip) -> float:
    if not ChanceForInfection_0(transmission_probability, neighbor_person, people_can_know_gossip):
        return 0

    c_transission, c_juicy = .8, .2

    return c_transission * transmission_probability + c_juicy * gossip.juicy

def ChanceForInfection_3(transmission_probability : float, current_person : Person, neighbor_person : Person, people_can_know_gossip : list[Person], gossip : Gossip) -> float:
    if not ChanceForInfection_0(transmission_probability, neighbor_person, people_can_know_gossip):
        return 0
    
    juicy_change = random.random() * current_person.gossip_modifier_constant
    c_juicy_change = .3
    gossip.juicy = (1 - c_juicy_change) * gossip.juicy + c_juicy_change * juicy_change

    return ChanceForInfection_2(transmission_probability, neighbor_person, people_can_know_gossip, gossip)

def ChanceForInfection_4(transmission_probability : float, G : nx.Graph, current_person : Person, neighbor_person : Person, people_can_know_gossip : list[Person], gossip : Gossip) -> float:
    if not ChanceForInfection_0(transmission_probability, neighbor_person, people_can_know_gossip):
        return 0
    
    if gossip.id in current_person.gossips_stopped: return 0

    c_gossip_stoppage, c_person_stoppage, c_friendship = .005, .005, .005
    try:
        friendship = G.edges[current_person.id, gossip.person_gossiped_about_id]['weight']
    except:
        friendship = 0
 
    chance_for_stoppage = c_gossip_stoppage * gossip.stoppable + c_person_stoppage * current_person.gossip_stoppage_constant + c_friendship * friendship
    if random.random() < chance_for_stoppage:
        current_person.gossips_stopped.append(gossip.id)
        return 0
    
    return transmission_probability

def ChanceForInfection_5(transmission_probability : float, current_person : Person, neighbor_person : Person, people_can_know_gossip : list[Person]) -> float:
    if not ChanceForInfection_0(transmission_probability, neighbor_person, people_can_know_gossip):
        return 0
    
    c_transission, c_person_speed_of_spread = .8, .2
   
    return c_transission * transmission_probability + c_person_speed_of_spread * current_person.speed_of_spread

def ChanceForInfection_6(transmission_probability : float, neighbor_person : Person, people_can_know_gossip : Person, gossip : Gossip) -> float:
    if not ChanceForInfection_0(transmission_probability, neighbor_person, people_can_know_gossip):
        return 0
    
    c_transission, c_number_of_times_heard = .8, .0001
   
    return c_transission * transmission_probability +  c_number_of_times_heard * neighbor_person.gossips_heard.get(gossip.id, 0)

def ChanceForInfection(transmission_probability : float, G : nx.Graph, current_person : Person, neighbor_person : Person, people_can_know_gossip : list[Person], gossip : Gossip) -> float:
    # Сегмент 0 - Базни модел
    if not neighbor_person.id in people_can_know_gossip or neighbor_person.state != 'Susceptible': return 0

    # Сегмент 1 - Зависност од друштвене повезаности
    weight = G.edges[current_person.id, neighbor_person.id]['weight']
    try:
        friendship = G.edges[current_person.id, gossip.person_gossiped_about_id]['weight']
    except:
        friendship = 0

    social_connection_factor = weight - friendship

    # Сегмент 2 + Привлачност информација
    juicy_factor = gossip.juicy

    # Сегмент 3 - Могућност модификације
    juicy_change = random.random() * current_person.gossip_modifier_constant
    c_juicy_change = .3
    gossip.juicy = (1 - c_juicy_change) * gossip.juicy + c_juicy_change * juicy_change

    # Сегмент 4 - Свесна одлука о преносу
    if gossip.id in current_person.gossips_stopped: return 0

    c_gossip_stoppage, c_person_stoppage, c_friendship = .005, .005, .005
    chance_for_stoppage = c_gossip_stoppage * gossip.stoppable + c_person_stoppage * current_person.gossip_stoppage_constant + c_friendship * friendship
    if random.random() < chance_for_stoppage:
        current_person.gossips_stopped.append(gossip.id)
        return 0

    # Сегмент 5 - Различита брзина ширења трачева
    speed_of_spread_factor = current_person.speed_of_spread

    # Сегмент 6 - Вишеструки независни извори
    number_of_times_heard_factor = neighbor_person.gossips_heard.get(gossip.id, 0)

    # Константе утицаја на пренос трача
    c_transmission_probability, c_social_connection, c_juicy, c_speed_of_spread, c_number_of_times_heard = .4999, .1, .2, .2, .0001

    total_chance = c_transmission_probability * transmission_probability 
    total_chance += c_social_connection * social_connection_factor 
    total_chance += c_juicy * juicy_factor 
    total_chance += c_speed_of_spread * speed_of_spread_factor 
    total_chance += c_number_of_times_heard * number_of_times_heard_factor
    return total_chance

def CalculateHubs(G : nx.Graph) -> None:
    # Прављење фајла са хабовима
    sorted_degree = sorted(G.degree(), key = lambda x: x[1], reverse = True)
    with open('hubs.txt', '+w') as file:
        for node, degree in sorted_degree:
            file.write(f"{node},{degree}\n")

def MakeInfectionPath(people_dict : dict[int : Person], gossip : Gossip):
    current_location = gossip.path_infected
    for person_id, person in people_dict.items():
        if person.state == "Infected":
            current_location = gossip.path_infected
            path = person.known_gossips[gossip.id]
            for location in path:
                try:
                    current_location = current_location[location]
                except:
                    current_location[location] = {}
                    current_location = current_location[location]
            
