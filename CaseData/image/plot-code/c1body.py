# coding=UTF-8

import numpy as np
import matplotlib.pyplot as plt

#set1
x11 = [0,
0,
0,
9,
57,
235,
290,
511,
593,
612,
656,
666,
976,
1028,
1031,
2660,
3311]
y11 = [0.9,
0.882212018455,
0.9,
0.55731081359,
0.789115267794,
0.426285921971,
0.401913081645,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05]
x12 = [3901, 3999]
y12 = [0.05, 0.05]
#set2
x2 = [
0,
7,
179,
185,
290,
616,
634,
717,
877,
1296,
1810,
1949,
2249,
2345,
2571,
3246,
3999]
y2 = [
0.387977915302,
0.499294017629,
0.05,
0.467624071298,
0.314110829757,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05,
0.05]
#set3
x3 = [
4,
9,
10,
16,
63,
66,
70,
161,
270,
451,
571,
641,
719,
721,
799,
916,
970,
2347,
3438,
3999]
y3 = [
0.759279336838,
0.779408432669,
0.9,
0.814559488984,
0.88337587134,
0.705724523659,
0.676861424077,
0.658128792455,
0.268295236588,
0.21309634744,
0.154166020185,
0.250098500529,
0.126243560972,
0.05,
0.0657903750491,
0.05,
0.05,
0.05,
0.05,
0.05]

# fig = plt.figure()
fig = plt.figure(figsize=(6,3.4))
ax1 = fig.add_subplot(111)

# ax1.set_title('Scatter Plot')

# plt.xlabel('X')

# plt.ylabel('Y')

size = 130
solid = 0.7

c11Value = ['r','r','r','b','r', 'b','r','b','b','b','b','b','b','b','b','b','b']
c12Value = ['b', 'b']
c13Value = ['g']
c2Value = ['b','r','b','r', 'r','b','b','b','b','b','b','b','b','b','b','b','b']
c3Value = ['b','b','g','b', 'r','g','g','r','b','b','b','b','b','b','b','b','b','b','b','b']

type1 = ax1.scatter(x11,y11,
	s=size,c=c11Value, marker='o', alpha=solid)
type2 = ax1.scatter(x12,y12,
	s=size,c=c12Value, marker='o', alpha=solid)
type3 = ax1.scatter(75,0.9,
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
ax1.set_ylabel('Case 1 body length (m)', fontsize=s)
ax1.legend((type2, type3, type1), (u'Bipeds', u'Bipedal-tripods', u'Tripods'), loc='upper right')

# plt.legend('x1')

plt.xticks(fontsize=s)
plt.yticks(fontsize=s)
plt.grid(alpha=0.6)
plt.savefig('/home/lima/Desktop/Case/image/heatmap1body.pdf', bbox_inches='tight')
plt.show()
