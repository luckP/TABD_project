from Taxi import *
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm

class Frame():
    def __init__(self, old_frame=None, taxis=None):
        if old_frame != None:
            taxi = old_frame.getTaxis()
        # elif taxis != None:
        #     self.taxi = taxis

        left_top = (-size, size)
        right_bottom = (size, -size)

        self.root = Node(left_top,right_bottom, 0)

        for t in taxis:
            self.root.add_taxi(t)


    def get_all_taxis(self):
        return self.root.get_all_taxis()

    def __str__(self):
        return str(self.root)

    def plot(self):
        self.root.plot()
        plt.show()
    def scan_100(self, x, y):
        return self.root.scan_100(x, y)

class Node():
    def __init__(self, left_top, right_bottom, depth):
        self.children = []
        self.left_top = left_top
        self.right_bottom = right_bottom
        self.taxis = []
        self.limit = 20
        self.depth = depth

    def add_taxi(self, taxi):
        self.taxis.append(taxi)
        self.deal_taxis()

        # print(self.depth)
        # print(abs(self.right_bottom[0]-self.left_top[0]))

        if len(self.taxis)>self.limit and ((abs(self.right_bottom[0]-self.left_top[0])>100) or (abs(self.left_top[1]-self.right_bottom[1])>100)) :
            x1, x2, y1, y2 = self.get_vertices()
            x_half = x1+(x2 - x1)/2
            y_half = y1-(y1 - y2)/2

            self.children.append(Node((x1, y1),(x_half, y_half), self.depth+1))  #left top
            self.children.append(Node((x_half, y1), (x2, y_half), self.depth+1)) # right top
            self.children.append(Node((x1, y_half), (x_half, y2), self.depth+1)) # bottom left
            self.children.append(Node((x_half, y_half), (x2, y2), self.depth+1)) # bottom rigth
            self.deal_taxis()

    def deal_taxis(self):
        if len(self.children)!=0:
            x1, x2, y1, y2 = self.get_vertices()
            x_half = x1+abs(x2 - x1)/2
            y_half = y1-abs(y1 - y2)/2

            for t in self.taxis:
                if t.coord[0]<x_half and t.coord[1]>y_half:
                    self.children[0].add_taxi(t)
                elif t.coord[0]>=x_half and t.coord[1]>y_half:
                    self.children[1].add_taxi(t)
                elif t.coord[0]<x_half and t.coord[1]<=y_half:
                    self.children[2].add_taxi(t)
                else:
                    self.children[3].add_taxi(t)
            self.taxis = []

    def get_all_taxis(self):
        taxis = self.taxis
        for c in self.children:
            taxis = taxis + c.get_all_taxis()

        return taxis

    def get_vertices(self):
        x1 = self.left_top[0]
        x2 = self.right_bottom[0]
        y1 = self.left_top[1]
        y2 = self.right_bottom[1]

        return x1, x2, y1, y2


    def __str__(self):
        s = ''
        for c in self.children:
            s += "\n    " + str(c)
        return str(self.left_top) + str(self.right_bottom) + str(len(self.taxis)) + s

    def plot(self):
        for t in self.taxis:
            t.plot()
        for c in self.children:
            c.plot()

        x1, x2, y1, y2 = self.get_vertices()
        plt.plot(np.array([x1, x2, x2, x1, x1]),np.array([y1, y1, y2, y2, y1]),c='k',ls='-',label='Rand', alpha=0.3)

    def scan_100(self, x, y):
        # verificar funcao
        taxis = []
        # dist = 100
        dist = 1000
        x1, x2, y1, y2 = self.get_vertices()

        x_half = x1+abs(x2 - x1)/2
        y_half = y1-abs(y1 - y2)/2

        circle_distance_x = abs(x-x_half)
        circle_distance_y = abs(y-y_half)

        if circle_distance_x <= abs(x1-x2)/2 or circle_distance_y <= abs(y1-y2)/2:
            for c in self.children:
                taxis += c.scan_100(x, y)
            for t in self.taxis:
                if np.sqrt( (t.coord[0]-x)**2 + (t.coord[1]-y)**2 )<dist:
                    taxis.append(t)
        return taxis
