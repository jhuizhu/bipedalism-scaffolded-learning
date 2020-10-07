# coding=UTF-8

import numpy as np
import matplotlib.pyplot as plt

#set1
x11 = [
0,
0,
13,
15,
95,
139,
258,
286,
570,
618,
822,
1002,
1126,
1392,
1707,
1938,
1957,
2486]
y11 = [
0.9,
0.882212018455,
0.150257244233,
0.647418452288,
0.499944763629,
0.37424548515,
0.228862667725,
0.164255513437,
0.142831057387,
0.05,
0.05,
0.090293551648,
0.05,
0.111777980904,
0.05,
0.05,
0.0530163616867,
0.0506565307533]

x12 = [4]
y12 = [0.771191069121]

x13 = [2927,3999]
y13 = [0.044092542261,0.044092542261]
#set2
x2 = [
1,
37,
57,
92,
155,
211,
232,
248,
330,
472,
563,
925,
1008,
1983,
2473,
2937,
3999]
y2 = [
0.517720286746,
0.0895120920947,
0.236782227719,
0.395317140144,
0.05,
0.12566992111,
0.05,
0.05,
0.05,
0.05,
0.05,
0.0620278302329,
0.05,
0.05,
0.0662790932846,
0.0445759028087,
0.0445759028087]
#set3
x3 = [
0,
28,
50,
89,
123,
131,
204,
245,
293,
353,
445,
815,
1103,
1724,
2503,
2640,
3978,
3999]
y3 = [
0.352903036695,

0.537238627479,
0.326269608884,
0.271035790946,
0.298157691821,
0.357302744495,
0.375273567148,
0.05,
0.0502765175385,
0.05,
0.0580307315005,
0.05,
0.05,
0.05,
0.05,
0.0663927742583,
0.05,
0.05]
x32 = [15]
y32 = [0.691168061471]
# fig = plt.figure()
fig = plt.figure(figsize=(6,3.4))
ax1 = fig.add_subplot(111)

# ax1.set_title('Scatter Plot')

# plt.xlabel('X')

# plt.ylabel('Y')

size = 130
solid = 0.7

c11Value = ['r','r','b','r','r', 'b','b','b','b','b','b','b','b','b','b','b','b','b']
c12Value = ['g']
c13Value = ['b','b']
c2Value = ['r','b','b','b', 'b','b','b','b','b','b','b','b','b','b','b','b','b']
c3Value = ['b','b','b','b', 'b','b','b','b','b','b','b','b','b', 'b','b','b','b','b']

type1 = ax1.scatter(x11,y11,
	s=size,c=c11Value, marker='o', alpha=solid)
type2 = ax1.scatter(x2,y2,
	s=size,c=c2Value, marker='o', alpha=solid)
type3 = ax1.scatter(x13,y13,
	s=size,c=c13Value, marker='o', alpha=solid)
type4 = ax1.scatter(x3,y3,
	s=size,c=c3Value, marker='o', alpha=solid)
type5 = ax1.scatter(x12,y12,
	s=size,c=c12Value, marker='o', alpha=solid)
type6 = ax1.scatter(x32,y32,
	s=size,c='b', marker='o', alpha=solid)

my_x_ticks = np.arange(0, 4001, 400)
my_y_ticks = np.arange(0, 0.95, 0.1)
ax1.set_xlim(-130, 4100)
ax1.set_ylim(0, 0.95)
ax1.set_xticks(my_x_ticks)
ax1.set_yticks(my_y_ticks)

s = 11
ax1.set_xlabel('Generations (-)', fontsize=s)
ax1.set_ylabel('Case 3 body length (m)', fontsize=s)
ax1.legend((type3, type5, type1), (u'Bipeds', u'Bipedal-tripods', u'Tripods'), loc='upper right')

# plt.legend('x1')
plt.xticks(fontsize=s)
plt.yticks(fontsize=s)
plt.grid(alpha=0.6)

plt.savefig('/home/lima/Desktop/Case/image/heatmap3body.pdf', bbox_inches='tight')
plt.show()
