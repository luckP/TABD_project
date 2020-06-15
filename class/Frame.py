from Taxi import *
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
import pandas as pd

class Frame():
    def __init__(self, previous_frame=None, taxis_coods=[]):
        self.previous_frame = previous_frame

        left_top = (-150000, 300000)
        right_bottom = (150000, -300000)

        # left_top = (-10000, 10000)
        # right_bottom = (10000, -10000)

        self.root = Node(left_top,right_bottom, 0)

        for i in range(len(taxis_coods)):
            if taxis_coods[i][0]!=0 or taxis_coods[i][1]!=0:
                self.root.add_taxi(Taxi(id=i, lat=taxis_coods[i][0], lgn=taxis_coods[i][1], state=0))


    def get_all_taxis(self):
        return self.root.get_all_taxis()

    def __str__(self):
        return str(self.root)

    def plot(self):
        self.root.plot()
        plt.show()

    def scan_100(self, x, y):
        return self.root.scan_100(x, y)

    def __len__(self):
        return len(self.root)

class Node():
    def __init__(self, left_top, right_bottom, depth):
        self.children = []
        self.left_top = left_top
        self.right_bottom = right_bottom
        self.taxis = []
        self.limit = 50
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

    def __add__(self):
        pass

    def __len__(self):
        l = 0
        for c in self.children:
            l+=len(c)
        return 1 + l

    def plot(self):
        for t in self.taxis:
            t.plot()
        for c in self.children:
            c.plot()

        x1, x2, y1, y2 = self.get_vertices()
        plt.plot(np.array([x1, x2, x2, x1, x1]),np.array([y1, y1, y2, y2, y1]),c='k',ls='-',label='Rand', alpha=0.3)

    def check_frontiers(self, x, y, dist_max):
        # http://ecalculo.if.usp.br/funcoes/trigonometricas/popups/rz_trigo_triret.htm
        x1, x2, y1, y2 = self.get_vertices()
        x_half = x1+abs(x2 - x1)/2
        y_half = y1-abs(y1 - y2)/2

        # ba1 = np.linalg.norm(np.array([x_half, y_half])-np.array([x_half, y2]))
        # bc2 = np.linalg.norm(np.array([x_half, y_half])-np.array([x, y]))
        # ba2 = np.linalg.norm(np.array([x_half, y_half])-np.array([x_half, y]))

        dist = np.sqrt((x-x_half)**2+(y-y_half)**2)
        dist2 = np.linalg.norm( np.array([x_half, y_half]) - np.array([x1, y1]))

        return dist <= dist_max + dist2
        # return dist <= dist_max + ((ba1*bc2)/ba2)
        # return x1<=x and x2>=x and y2<=y and y1>=y

    def scan_100(self, x, y):
        taxis = []
        # dist = 100
        dist_max = 100
        x1, x2, y1, y2 = self.get_vertices()

        x_half = x1+abs(x2 - x1)/2
        y_half = y1-abs(y1 - y2)/2

        if self.check_frontiers(x, y, dist_max):
            # plt.plot(np.array([x1, x2, x2, x1, x1]),np.array([y1, y1, y2, y2, y1]), markersize=2, color="red" ,c='k',ls='-',label='Rand', alpha=.1)
            # plt.plot(np.array([x, x_half]), np.array([y, y_half]), color="green")
            for c in self.children:
                taxis += c.scan_100(x, y)
            for t in self.taxis:
                # t.plot(markersize=3, color='green')
                if np.sqrt( (t.coord[0]-x)**2 + (t.coord[1]-y)**2 )<dist_max:
                    taxis.append(t)
        return taxis

#
# # teste frame
# df = pd.read_csv('one_time.csv')
# df['0'] = df['0'].map(lambda x: eval(x))
# taxis = [Taxi(i, df['0'][i][0], df['0'][i][1], random.choices([0,1])[0], random.choices([1,2,3,4])[0]) for i in range(len(df['0'])) if(df['0'][i][0]!=0 or df['0'][i][1]!=0)]
#
# f = Frame(taxis=taxis)
# # id = int(len(taxis)/len(taxis))
# # tt = []
# # count = 0
# # for t in taxis:
# #     ttt = []
# #     ttt = f.scan_100(t.coord[0], t.coord[1])
# #     if len(ttt)>0:
# #         t.plot(color='blue', markersize=3, alpha=1)
# #         count+=1
#
# # for t in tt:
# #     t.plot(color='red', markersize=3)
# # taxis[id].plot(color='blue', markersize=3, alpha=1)
#
# # print(count)
# print(len(f))
# plt.rcParams['figure.figsize'] = (11, 11)
# f.plot()
# # plt.show()
