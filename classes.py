class Person:
    def __init__(self, person_id):
        self.id = person_id
        self.state = 'Susceptible'
        self.known_gossips = {}

class Gossip:
    def __init__(self, gossip_id, person_gossiped_about_id):
        self.id = gossip_id
        self.person_gossiped_about_id = person_gossiped_about_id