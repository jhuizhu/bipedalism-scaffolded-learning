# coding=UTF-8

import numpy as np
import matplotlib.pyplot as plt

#set1
x11 = [
0,
0,
15,
23,
39,
324,
437,
437,
479,
490,
514,
537,
557,
724,
748,
761,
825]
y11 = [
0.9,
0.882212018455,
0.543548446404,
0.9,
0.610676053951,
0.277446719996,
0.151747732479,
0.05,
0.05,
0.0583462059488,
0.0944818827228,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05]

x12 = [5]
y12 = [0.419002270417]

x13 = [1362,3999]
y13 = [0.0589642060194,0.0589642060194]
#set2
x2 = [
4,
29,
88,
128,
255,
365,
425,
635,
719,
721,
726,
750,
773,
808,
937,
976,
1009,
1051,
1052,
1165,
1587,
1900,
3999]
y2 = [
0.787000793351,
0.604169890486,
0.721464178202,
0.583145596274,
0.419099705962,
0.662929355903,
0.607883953458,
0.573989271062,
0.7,
0.7,
0.405452725819,
0.545347224467,
0.492821258128,
0.453209399024,
0.420180400486,
0.614458206703,
0.5,
0.5,
0.5,
0.5,
0.3,
0.3,
0.3]
#set3
x3 = [
1,
10,
29,
151,
775,
989,
1368,
3999]
y3 = [
0.727102963911,
0.496891020705,
0.77544824684,
0.607904646008,
0.7,
0.7,
0.5,
0.5]

# fig = plt.figure()
fig = plt.figure(figsize=(6,3.4))
ax1 = fig.add_subplot(111)
# ax1.set_title('Scatter Plot')
# plt.xlabel('X')
# plt.ylabel('Y')

size = 130
solid = 0.7

c11Value = ['r','r','b','r','b', 'b','b','b','b','b','b','b','b','b','b','b','b']
c12Value = ['g']
c13Value = ['b']
c2Value = ['r','b','b','r', 'r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r','r']
c3Value = ['g','b','r','r', 'r','r','r', 'r']

type1 = ax1.scatter(x11,y11,
	s=size,c=c11Value, marker='o', alpha=solid)
type2 = ax1.scatter(x12,y12,
	s=size,c=c12Value, marker='o', alpha=solid)
type3 = ax1.scatter(x13,y13,
	s=size,c=c13Value, marker='o', alpha=solid)
type4 = ax1.scatter(x2,y2,
	s=size,c=c2Value, marker='o', alpha=solid)
type5 = ax1.scatter(x3,y3,
	s=size,c=c3Value, marker='o', alpha=solid)
my_x_ticks = np.arange(0, 4001, 400)
my_y_ticks = np.arange(0, 0.95, 0.1)
ax1.set_xlim(-130, 4100)
ax1.set_ylim(0, 0.95)
ax1.set_xticks(my_x_ticks)
ax1.set_yticks(my_y_ticks)

s = 11
ax1.set_xlabel('Generations (-)', fontsize=s)
ax1.set_ylabel('Case 2 body length (m)', fontsize=s)
ax1.legend((type3, type2, type1), (u'Bipeds', u'Bipedal-tripods', u'Tripods'), loc='upper right')

# plt.legend('x1')
plt.xticks(fontsize=s)
plt.yticks(fontsize=s)
plt.grid(alpha=0.6)

plt.savefig('/home/lima/Desktop/Case/image/heatmap2body.pdf', bbox_inches='tight')
plt.show()

