class Person:
    def __init__(self, person_id, gossip_modifier_constant):
        self.id = person_id
        self.state = 'Susceptible'
        self.known_gossips = {}
        self.gossip_modifier_constant = gossip_modifier_constant

class Gossip:
    def __init__(self, gossip_id, person_gossiped_about_id, juicy):
        self.id = gossip_id
        self.person_gossiped_about_id = person_gossiped_about_id
        self.juicy = juicy