import networkx as nx
import matplotlib.pyplot as plt
import random
from classes import Person, Gossip

def main():
    # параметри за симулацију
    num_initial_infected = 1 
    transmission_probability = 0.3 
    simulation_days = 30

    # параметри за мрежу
    num_people = 500
    k_param = 4
    p_param = 0.1

    # прављење мреже
    people = []
    for i in range(num_people):
        people.append(Person(i))
    people_dict = {person.id: person for person in people}
    G = nx.watts_strogatz_graph(num_people, k_param, p_param) # модел малих светова за прављење мреже

    # прављење трача
    gossip_id_counter = 0
    person_gossiped_about_id = random.choice([p.id for p in people])
    main_gossip = Gossip(gossip_id_counter, person_gossiped_about_id)
    gossip_id_counter += 1

    # постављање почетно заражених особа
    initial_infected_ids = random.sample([p.id for p in people], num_initial_infected)
    for person_id in initial_infected_ids:
        people_dict[person_id].state = 'Infected'
        people_dict[person_id].known_gossips[main_gossip.id] = main_gossip.person_gossiped_about_id

    # чување параметара ширења кроз време
    infected_count_over_time = []

    # симулација
    for day in range(simulation_days):
        newly_infected_ids = [] # листа људи који су данас заражени

        for person_id, current_person in people_dict.items():
            # ако је тренутна особа заражена шири се трач њеним суседима
            if current_person.state == 'Infected':
                neighbors = list(G.neighbors(person_id))

                for neighbor_id in neighbors:
                    neighbor_person = people_dict[neighbor_id]
                    # ако је тренутни сусед незаражен, постоји шанса да се зарази
                    if neighbor_person.state == 'Susceptible':
                        if random.random() < transmission_probability:
                            newly_infected_ids.append(neighbor_id)
                            neighbor_person.known_gossips[main_gossip.id] = main_gossip.person_gossiped_about_id

        # чување информација новозаражених на крају дана
        for person_id in newly_infected_ids:
            people_dict[person_id].state = 'Infected'

        # чување метрика
        current_infected_count = sum(1 for person in people if person.state == 'Infected')
        infected_count_over_time.append(current_infected_count)

        print(f"Дан {day+1}:  \t Број заражених: {current_infected_count}")


    # испис метрика на крају симулације

    ## укупан обим заразе
    total_infected_percentage = (infected_count_over_time[-1] / num_people) * 100
    print(f"\nУкупни обим ширења: {total_infected_percentage:.2f}% популације је сазнало трач.")

    ## време до 50% заразе
    fifty_percent_threshold = num_people * 0.5
    time_to_50_percent = -1
    for day, count in enumerate(infected_count_over_time):
        if time_to_50_percent == -1 and count >= fifty_percent_threshold:
            time_to_50_percent = day + 1
    if time_to_50_percent != -1:
        print(f"Време док трач не дође до 50% популације: {time_to_50_percent} дана.")
    else:
        print("Трач није достигао 50% популације у току симулације.")

    ## време до 90% заразе
    ninety_percent_threshold = num_people * 0.9
    time_to_90_percent = -1
    for day, count in enumerate(infected_count_over_time):
        if time_to_90_percent == -1 and count >= ninety_percent_threshold:
            time_to_90_percent = day + 1
    if time_to_90_percent != -1:
        print(f"Време док трач не дође до 90% популације: {time_to_90_percent} дана.")
    else:
        print("Трач није достигао 90% популације у току симулације.")

    ## приказ криве ширења
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, simulation_days + 1), infected_count_over_time, marker='o', linestyle='-', color='blue')
    plt.title('Ширење трача кроз време (модел 1)')
    plt.xlabel('Дан симулације')
    plt.ylabel('Број особа које знају трач')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main()