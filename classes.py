class Person:
    def __init__(self, person_id, gossip_modifier_constant, gossip_stoppage_constant, speed_of_spread):
        self.id = person_id
        self.state = 'Susceptible'
        self.known_gossips = {}
        self.gossip_modifier_constant = gossip_modifier_constant
        self.gossip_stoppage_constant = gossip_stoppage_constant
        self.gossips_stopped = []
        self.speed_of_spread = speed_of_spread
        self.gossips_heard = {}

class Gossip:
    def __init__(self, gossip_id, person_gossiped_about_id, juicy, stoppable):
        self.id = gossip_id
        self.person_gossiped_about_id = person_gossiped_about_id
        self.juicy = juicy
        self.stoppable = stoppable
        self.path_infected = {}