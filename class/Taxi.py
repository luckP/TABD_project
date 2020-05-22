import matplotlib.pyplot as plt

class Taxi():
    def __init__(self, id, lat, lgn, infec, state, speed=0):
        self.id = id
        self.coord = (lat, lgn)
        self.infec = infec
        self.state = state #PICKUP PAUSE BUSY FREE
        self.speed = speed

    def __str__(self):
        return '( id: ' + str(self.id) + ', lat: ' + str(self.coord[0]) + ', lgn: ' + str(self.coord[1]) + 'infec: ' + str(self.infec) + ',state: ' + str(self.state) + ')'

    def plot(self, color='black', markersize=2):
        # if self.infec == 1:
        #     color = 'red'
        plt.plot([self.coord[0]], [self.coord[1]], 'ro', color=color, markersize=markersize)
