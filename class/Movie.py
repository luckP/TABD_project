from Frame import *

class Movie():
    def __init__(self, taxis_matrix=[]):
        self.index = 0

        if len(taxis_matrix)>0:
            self.frames = [Frame(taxis_coods = taxis_matrix[0])]
        for i in range(1, len(taxis_matrix)):
            self.add_frame(Frame(previous_frame=self.frames[i-1], taxis_coods=taxis_matrix[i]))

    def add_frame(self, frame):
        self.frames.append(frame)

    def plot_frame(self, i):
        self.frames[i].plot()

    def num_nodes_frame(self, i):
        return len(self.frames[i])

    def __str__(self):
        return 'Nº frames: ' + str(len(self.frames)) + ' | Index: ' + str(self.index)
