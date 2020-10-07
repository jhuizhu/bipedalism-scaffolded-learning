# coding=UTF-8
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib as mpl
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import ConnectionPatch

fig = plt.figure(figsize=(7,6.6))
ax = fig.add_subplot(111)

# unrate = pd.read_csv('/home/lima/Desktop/Case/image/plot-code/gait_data/b_vertical displacement.csv')
unrate = pd.read_csv('/home/lima/Desktop/Case/image/plot-code/gait_data/t_vertical velocity.csv') 
# unrate = pd.read_csv('/home/lima/Desktop/Case/image/plot-code/gait_data/b_horizontal velocity.csv')


# unrate1 = pd.read_csv('biped_distance.csv') 
print(unrate.head()) 

first_twelve = unrate 

# ax.plot(first_twelve['Time (ms)']/1000, speed,color='royalblue', linestyle='-', alpha=1.0,label='Best Biped', linewidth=3) 
# ax.plot(first_twelve['Time (ms)']/1000, speed,color='indianred', linestyle='-', alpha=1.0,label='Best Tripod', linewidth=3)

# first_twelve['Time (ms)'] = filter(lambda x:x%200 == 0, first_twelve['Time (ms)'])
# ax.plot(first_twelve['Time (ms)']/1000, first_twelve['Trajectory 1']/1.16, color='royalblue', linestyle='-', alpha=1.0,label='Best Biped', linewidth=3) 
# ax.plot(first_twelve['Time (ms)']/1000, first_twelve['Trajectory 1']/0.404,color='indianred', linestyle='-', alpha=1.0,label='Best Tripod', linewidth=3)
ax.plot(first_twelve['Time (ms)']/1000, 100*first_twelve['Trajectory 1']/0.404,color='indianred', linestyle='-', alpha=1.0,label='Best Tripod', linewidth=3)

# z = np.polyfit(first_twelve['Time (ms)']/1000,first_twelve['Trajectory 1']/1.16, 4)
# z = np.polyfit(first_twelve['Time (ms)']/1000,first_twelve['Trajectory 1']/0.404, 1)

# p = np.poly1d(z)

# ax.plot(first_twelve['Time (ms)']/1000, p(first_twelve['Time (ms)']/1000),color='royalblue', linestyle='-', alpha=1.0,label='Best Biped', linewidth=3) 
# ax.plot(first_twelve['Time (ms)']/1000, p(first_twelve['Time (ms)']/1000),color='indianred', linestyle='-', alpha=1.0,label='Best Tripod', linewidth=3)

# ax.plot(first_twelve['Time (ms)']/1000, first_twelve['Trajectory 1']/1.16,color='royalblue', linestyle='-', alpha=1.0,label='Best Biped', linewidth=3) 
# ax.plot(first_twelve['Time (ms)']/1000, first_twelve['Trajectory 1'],color='indianred', linestyle='-', alpha=1.0,label='Best Tripod', linewidth=3)

# ax.plot(unrate1['Time (ms)'], unrate1['Trajectory biped'],'b',alpha=0.7,label='Best Biped') 
# ax.plot(unrate1['Time (ms)'], unrate1['Trajectory tripod'],'r', alpha=0.7,label='Best Tripod')

# ax.set_xlim(-250, 15250)    
# ax.set_ylim(-0.8, 22)    
# my_x_ticks = np.arange(0, 2500, 15000)
# my_y_ticks = np.arange(-0.40, 0.1,0.1)
# ax.set_xticks(my_x_ticks)
# ax.set_yticks(my_y_ticks)
# plt.xticks(rotation=30) 

s = 22
plt.xticks(fontsize=s)
plt.yticks(fontsize=s)
# for CoG
# my_x_ticks = np.arange(-0.0, 15.1, 2.5)
# my_y_ticks = np.arange(-0.3, 0.01, 0.1)
# ax.set_xlim(-0.7, 15.7)
# ax.set_ylim(-0.37, 0.07)
# ax.set_xticks(my_x_ticks)
# ax.set_yticks(my_y_ticks)

# for hv1
# my_x_ticks = np.arange(-0.0, 15.1, 2.5)
# my_y_ticks = np.arange(-4.0, 8.01, 2)
# ax.set_xlim(-0.7, 15.7)
# ax.set_ylim(-4.7, 8.7)
# ax.set_xticks(my_x_ticks)
# ax.set_yticks(my_y_ticks)

# # for hv2
# my_x_ticks = np.arange(-0.0, 15.1, 2.5)
# my_y_ticks = np.arange(-0.04, 0.07, 0.02)
# ax.set_xlim(-0.7, 15.7)
# ax.set_ylim(-0.05, 0.07)
# ax.set_xticks(my_x_ticks)
# ax.set_yticks(my_y_ticks)

# for vv1
my_x_ticks = np.arange(-0.0, 15.1, 2.5)
my_y_ticks = np.arange(-6.0, 2.01, 1)
ax.set_xlim(-0.7, 15.7)
ax.set_ylim(-6.3, 2.3)
ax.set_xticks(my_x_ticks)
ax.set_yticks(my_y_ticks)

# for vv2
# my_x_ticks = np.arange(-0.0, 15.1, 2.5)
# my_y_ticks = np.arange(-6.0, 2.01, 2)
# ax.set_xlim(-0.7, 15.7)
# ax.set_ylim(-6.5, 2.5)
# ax.set_xticks(my_x_ticks)
# ax.set_yticks(my_y_ticks)


# ax.legend(loc='upper left', fontsize=20) 
# ax.legend()
ax.set_xlabel('Interaction time (s)',fontsize=s) 
# ax.set_ylabel('Relative horizontal velocity (ll/s)',fontsize=s) 
ax.set_ylabel('Relative vertical velocity (ll/s)',fontsize=s) 
# ax.set_ylabel('Relative CoG position (ll)',fontsize=s) 
# plt.title('Trajectory') 

# ax = plt.gca()  
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
# # set(gca,'ytick',y)
# # set(gca,'yTickLabel',num2str(get(gca,'yTick')','%.2f'))
# # ax.xaxis.get_major_formatter().set_powerlimits((0,2)) 
# # ax.yaxis.get_major_formatter().set_powerlimits((2,-1)) 
# axins = inset_axes(ax, width="40%", height="30%", loc='lower left',
#                    bbox_to_anchor=(0.3, 0.2, 1, 1), 
#                    bbox_transform=ax.transAxes)

# x_axis_data = first_twelve['Time (ms)']/1000
# reward_demaddpg5 = first_twelve['Trajectory 1']/0.404
# # reward_demaddpg5 = first_twelve['Trajectory 1']

# axins.plot(x_axis_data, reward_demaddpg5, color='indianred', linestyle='-', alpha=1.0,label='Best Tripod', linewidth=3)

# zone_left = 450
# zone_right = 600


# x_ratio = 1 
# y_ratio = 1 


# xlim0 = x_axis_data[zone_left]-(x_axis_data[zone_right]-x_axis_data[zone_left])*x_ratio
# xlim1 = x_axis_data[zone_right]+(x_axis_data[zone_right]-x_axis_data[zone_left])*x_ratio


# y = np.hstack(reward_demaddpg5[zone_left:zone_right])
# ylim0 = np.min(y)-(np.max(y)-np.min(y))*y_ratio
# ylim1 = np.max(y)+(np.max(y)-np.min(y))*y_ratio


# axins.set_xlim(xlim0, xlim1)
# axins.set_ylim(ylim0, ylim1)


# tx0 = xlim0
# tx1 = xlim1
# ty0 = ylim0
# ty1 = ylim1
# sx = [tx0,tx1,tx1,tx0,tx0]
# sy = [ty0,ty0,ty1,ty1,ty0]
# ax.plot(sx,sy,"black")


# xy = (xlim0,ylim0)
# xy2 = (xlim0,ylim1)
# con = ConnectionPatch(xyA=xy2,xyB=xy,coordsA="data",coordsB="data",
#         axesA=axins,axesB=ax)
# axins.add_artist(con)

# xy = (xlim1,ylim0)
# xy2 = (xlim1,ylim1)
# con = ConnectionPatch(xyA=xy2,xyB=xy,coordsA="data",coordsB="data",
#         axesA=axins,axesB=ax)
# axins.add_artist(con)

# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.grid(alpha=0.6)

# plt.rc('font', family='serif', size=17)
# plt.grid(axis="x", alpha=0.5)
plt.grid(alpha=0.6)
plt.savefig('/home/lima/Desktop/Case/image/plot-code/gait_data/new_gait/trv.pdf', bbox_inches='tight')
plt.show() 