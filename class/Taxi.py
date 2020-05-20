class Taxi():
    def __init__(self, id, lat, lgn, infec, state):
        self.id = id
        self.coord = (lat, lgn)
        self.infec = infec
        self.state = state #PICKUP PAUSE BUSY FREE