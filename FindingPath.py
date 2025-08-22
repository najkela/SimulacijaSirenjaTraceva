from utils import *

def main():
    # Параметри за симулацију
    transmission_probability = 0.02
    simulation_days = 25

    # Учитавање графа
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

    # Прављење трача
    gossip_id_counter = 0
    person_gossiped_about_id = random.choice(list(people_dict.keys()))
    gossip_juicy = random.random()
    gossip_stoppable = random.random()
    main_gossip = Gossip(gossip_id_counter, person_gossiped_about_id, gossip_juicy, gossip_stoppable)
    gossip_id_counter += 1

    # Покретање симулације
    max_infected_count, infected_count_over_time = RunSingleSimulation(G, people_dict, transmission_probability, simulation_days, main_gossip)

    MakeInfectionPath(people_dict, main_gossip)
    print(main_gossip.path_infected)

if __name__ == "__main__":
    main()