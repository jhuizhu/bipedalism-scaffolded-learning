import matplotlib.pyplot as plt
import math
import seaborn as sns
import numpy as np
def getdata():      
    cond1 = [0,
0.315952227,
0.331364619,
0.377291261,
0.45196638,
0.988789888,
1.522575028,
2.265473889,
3.013542499,
3.804932149,
4.640070688,
5.382440174,
6.032299184,
6.758864779,
7.857888124,
8.835612574,
9.632939646,
10.26982406,
11.0866599,
11.8465302,
12.60035105,
13.30886829,
13.95919613,
14.80761647,
15.6505182,
16.44607606,
17.40234084,
17.94041186,
19.15777083,
20.27009948,
21.10924388
]

    cond2 = [0,
0.534272154,
0.646874096,
0.661420252,
0.675870045,
1.021744394,
1.462281219,
2.019642207,
2.821094404,
3.555295571,
4.179471564,
4.830943692,
5.486826311,
5.951212254,
6.506481116,
7.042642234,
7.841989271,
8.377716063,
9.161988354,
9.670064144,
10.08148365,
10.49190029,
11.06815642,
11.53967666,
12.08802095,
12.60534606,
13.01226504,
13.5523093,
14.09736486,
14.74138232,
15.33352466
]    

    return cond1, cond2

data = getdata()
fig = plt.figure()
xdata = [0,
500,
1000,
1500,
2000,
2500,
3000,
3500,
4000,
4500,
5000,
5500,
6000,
6500,
7000,
7500,
8000,
8500,
9000,
9500,
10000,
10500,
11000,
11500,
12000,
12500,
13000,
13500,
14000,
14500,
15000
]
linestyle = ['-', '-']
marker = ['s', 'o']
color = ['blue', 'red']
label = ['Best Biped', 'Best Tripod']
sns.set(style="darkgrid", font_scale=1)

for i in range(2):    
    sns.tsplot(time=xdata, data=data[i], color=color[i], linestyle=linestyle[i], marker=marker[i],condition=label[i])
    # print(xdata)
    # print(data[i])
plt.xlim(-250, 15250)    
plt.ylim(-0.8, 22)    
my_x_ticks = np.arange(0, 15001, 2500)
my_y_ticks = np.arange(0, 22.1, 2)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
# plt.xticks(rotation=30) 
plt.legend() 
plt.xlabel('Interaction time (ms)') 
plt.ylabel('Distnace/leg length (-)') 
# plt.title('Trajectory') 
# plt.grid(axis="y")
# plt.grid()
plt.grid(alpha=0.4)
plt.rc('font', family='serif', size=17)
plt.savefig('/home/lima/Desktop/Case/image/fitnessplot.pdf', bbox_inches='tight')
plt.show()